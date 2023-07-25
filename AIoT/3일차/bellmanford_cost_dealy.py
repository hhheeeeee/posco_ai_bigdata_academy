import time
from collections import defaultdict
from typing import DefaultDict

from router_lab import NodeCustomBase, is_valid_ip


class DBFRoutingPacket:
    def __init__(self, src: str, routing_table: dict[str, float]):
        self.src = src
        self.routing_table: dict[str, float] = routing_table

    def to_bytes(self) -> bytes:
        return (
            b"routing\n"
            + self.src.encode()
            + b"\n"
            + b"\n".join(f"{dst} {cost}".encode() for dst, cost in self.routing_table.items())
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> "DBFRoutingPacket":
        lines = data.split(b"\n")
        src = lines[1].decode()
        routing_table = {}
        for line in lines[2:]:
            if not line:
                continue
            dst, cost = line.decode().split()
            assert is_valid_ip(dst), "Invalid IP, maybe bit corruption!"
            routing_table[dst] = float(cost)
        return cls(src, routing_table)


class DataPacket:
    def __init__(self, src: str, dst: str, hop: int, data: bytes):
        self.src = src
        self.dst = dst
        self.hop = hop
        self.data = data

    def to_bytes(self) -> bytes:
        return (
            b"data\n"
            + self.src.encode()
            + b"\n"
            + self.dst.encode()
            + b"\n"
            + str(self.hop).encode()
            + b"\n"
            + self.data
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> "DataPacket":
        lines = data.split(b"\n")
        src = lines[1].decode()
        dst = lines[2].decode()
        hop = int(lines[3].decode())
        data = lines[4]
        return cls(src, dst, hop, data)

class NullPacket:
    def __init__(self, is_ack: bool, timestamp: float):
            self.is_ack = is_ack
            self.timestamp = timestamp

    def to_bytes(self) -> bytes:
        return b"null\n" + str(int(self.is_ack)).encode() + b"\n" + str(self.timestamp).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> "NullPacket":
        lines = data.split(b"\n")
        is_ack = bool(int(lines[1].decode()))
        timestamp = float(lines[2].decode())
        return cls(is_ack, timestamp)


class DistributedBellmanFordNodeImpl(NodeCustomBase):
    async def every_1s(self):
        #record_table이 라우팅테이블 만드는 함수, 본인꺼는 self.routing_table에 있다
        for dst, (next_hop, cost) in self.routing_table.items():
            self.record_table(dst, next_hop=next_hop, cost=cost)  #visualize 하기 위한 목적

        # 10~30초 동안 distance 벡터를 전파한다.
        if self.send_vector_timer >= 10 and self.send_vector_timer <= 30:
            await self.broadcast(
                DBFRoutingPacket(  #본인 ip , source, routing table
                    self.ip, {dst: cost for dst, (next_hop, cost) in self.routing_table.items()}
                ).to_bytes()
            )
        elif self.send_vector_timer < 10: # 앞의 10초 동안은 NullPacket으로 인접노드와의 패킷전송딜레이를 구한다.
            await self.broadcast(NullPacket(False, time.time()).to_bytes()) #자기 자신의 라우팅 테이블을 전파
        self.send_vector_timer += 1

    async def main(self):
        self.routing_table: DefaultDict[str, tuple[str, float]] = defaultdict(
            lambda: ("", float("inf")) #빈 라우팅 테이블 만들기
        )
        self.routing_table[self.ip] = (self.ip, 0.0) # 내가 나에게 보내는건 cost가 0이다
        self.adjacent_delay: dict[str, float] = {}
        await self.broadcast(NullPacket(False, time.time()).to_bytes())

    async def on_recv(self, src_1hop: str, data: bytes): # 라우팅 패킷을 받았다. 바이트를 받은것이므로 분리해줘야함
        if data.startswith(b"routing"):
            pkt = DBFRoutingPacket.from_bytes(data) # 다른 노드의 라우팅테이블인데 이게 본인 라우팅테이블에 없으면 추가한다
            if pkt.src not in self.routing_table:
                self.routing_table[pkt.src] = (src_1hop, self.adjacent_delay[src_1hop])
            # 받은 distance 벡터를 바탕으로 라우팅테이블을 업데이트 해준다   
            for dst, cost in pkt.routing_table.items():
                if (
                        dst not in self.routing_table 
                        or self.routing_table[dst][1] > cost + self.adjacent_delay[src_1hop]
                    ):
                    self.routing_table[dst] = (src_1hop, cost + self.adjacent_delay[src_1hop])
        elif data.startswith(b"data"):
            pkt = DataPacket.from_bytes(data)
            if pkt.dst == self.ip:  #만약 목적지가 본인이다. 
                self.log.info(f"Received from {pkt.src} with {pkt.hop} hops: {pkt.data}") #어디에서 몇 홉으로 왔는지 알려주고
                self.record_stat(routed_hops = pkt.hop)
            else: #내가 목적지가 아니라면 dest를 뽑은 뒤 라우팅테이블에 따라서 unicast를 통해 다음 목적지로 보낸다.
                next_hop, cost = self.routing_table[pkt.dst] 
                self.log.info(f"Sending to {pkt.dst} vis {next_hop} (cost: {cost})")
                await self.unicast(
                    next_hop, DataPacket(self.ip, pkt.dst, pkt.hop + 1, pkt.data).to_bytes()
                )
        elif data.startswith(b"null"):
            pkt = NullPacket.from_bytes(data)
            if pkt.is_ack:
                self.adjacent_delay[src_1hop] = time.time() - pkt.timestamp
            else:
                await self.unicast(src_1hop, NullPacket(True, time.time()).to_bytes())
        else:
            self.log.warning(f"Unknown packet type!")

    async def on_queue(self, dst: str, data: bytes): # 데이터 패킷을 어떻게 만들어낼지
        if dst in self.routing_table:
            next_hop, cost = self.routing_table[dst] #라우팅테이블에 있으면 그걸 뽑아내서 unicast로 테이터 패킷을 보낸다
            self.log.info(f"Sendinf to {dst} via {next_hop} (cost: {cost})")
            await self.unicast(next_hop, DataPacket(self.ip, dst, 1, data).to_bytes())
        else:
            self.log.info(f"Cannot send to {dst} (no route!)") #만약 목적지가 본인 라우팅테이블에 없으면!

    def on_start(self):
        self.send_vector_timer = 0
