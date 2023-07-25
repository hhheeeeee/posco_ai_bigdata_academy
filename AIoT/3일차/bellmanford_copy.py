from collections import defaultdict
from typing import DefaultDict

from router_lab import NodeCustomBase, is_valid_ip


class DBFRoutingPacket:
    def __init__(self, src: str, routing_table: dict[str, float]):
        self.src = src
        self.routing_table: dict[str, float] = routing_table

    def to_bytes(self) -> bytes:
        return (
            b"routing\n" #라우팅은 헤더 같이 라우팅 패키지라는거 알려주고
            + self.src.encode()  ##소스 아이피
            + b"\n"
            + b"\n".join(f"{dst} {cost}".encode() for dst, cost in self.routing_table.items()) #딕셔너리를 바이트로 저장하기 위한 코드
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
            assert is_valid_ip(dst), "Invalid IP, maybe bit corruption!" #시뮬레이션 안에 있는 아이피인가를 확인한다., 왜냐면 시뮬레이션에서 bit corruption rate가 잇어서
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


    @classmethod
    def from_bytes(cls, data: bytes) -> "DataPacket":
        lines = data.split(b"\n")
        src = lines[1].decode()
        dst = lines[2].decode()
        hop = int(lines[1].decode())
        data = lines[4]
        return cls(src, dst, hop, data)


class DistrbuteBellmanFordNodeImpl(NodeCustomBase):
    async def every_1s(self):
        if self.send_vector_timer < 10:  # 0 to 9
            for neighbor_ip in self.adjacentDelay:  # Iterate over adjacent nodes
                timestamp = await self.measure_delay(neighbor_ip)  # Measure the delay to the neighbor node
                null_pkt = NullPacket(is_ack=False, timestamp=timestamp)
                await self.unicast(neighbor_ip, null_pkt.to_bytes())  # Send NullPacket to the neighbor node
        elif self.send_vector_timer < 20:  # 10 to 19
            # log routing table
            for dst, (next_hop, cost) in self.routing_table.items():
                self.record_table(dst, next_hop=next_hop, cost=cost)

            # send distance vector
            await self.broadcast(
                DBFRoutingPacket(
                    self.ip, {dst: cost for dst, (next_hop, cost) in self.routing_table.items()}
                ).to_bytes()
            )
        self.send_vector_timer += 1

    async def on_recv(self, src_1hop: str, data: bytes): #라우팅 패킷을 받앗다, 바이트를 받은거니까 그거를 분리해줘야댐
        if data.startswith(b"routing"):
            pkt = DBFRoutingPacket.from_bytes(data) #어떤 놈의 라우팅테이블일건데 그게 본인 라우팅테이블에 없으면 추가해준다.
            if pkt.src not in self.routing_table:
                self.routing_table[pkt.src] = (src_1hop, self.adjacentDelay[src1_hop])
            for dst, cost in pkt.routing_table.items(): # 그리고 그 안에 값들을 보고 dest가 받은 패킷의 라우팅테이블이니까 나랑 인접한 노드가 아닐 것임.
                if dst not in self.routing_table or self.routing_table[dst][1] > cost + 1: # cost가 라우팅테이블 안에 있는 cost보다 크면!! = 더 짧은 길이 있으면 라우팅 테이블을 업데이트 해라
                    self.routing_table[dst] = (src_1hop, cost + 1) #인접한데서 패킷이 왔으니까 인접한데서 온게 1 hop이니까 1 더해준거
        elif data.startswith(b"data"):
            pkt = DataPacket.from_bytes(data)
            if pkt.dst == self.ip: #만약 목적지가 본인이다....
                self.log.info(f"Received from {pkt.src} with {pkt.hop} hops : {pkt.data}")#어디에서 몇 홈으로 왔는지 알려주고
                self.record_stat(routed_hops=pkt.hop)
            else: #목적지가 본인이 아니라면 dest를 뽑아서 다음 홉으로 보낸다(라우팅테이블에 따라서, unicast 목적지로 보낸다)
                next_hop, cost = self.routing_table[pkt.dst]
                self.log.info(f"Sending to {pkt.dst} via {next_hop} (cost: {cost})") 
                await self.unicast(
                    next_hop, DataPacket(self.ip, pkt.dst, pkt.hop + 1, pkt.data).to_bytes() #나를 거쳐갔으니까 hop에 +1 하는거임
                )
        else:
            self.log.warning(f"Unknown packet type!")

    async def on_queue(self, dst: str, data: bytes): #이 데이터 패킷을 만들어냇는데 
        if dst in self.routing_table:
            next_hop, cost = self.routing_table[dst] # 라우팅테이블에 있으면 그걸 뽑아내서 unicast로 데이터패킷을 보낸다
            self.log.info(f"Sending to {dst} via {next_hop} (cost: {cost})")
            await self.unicast(next_hop, DataPacket(self.ip, dst, 1, data).to_bytes()) #cost가 1인 이유는 본인이 생성을 했으니까!!
        else:
            self.log.info(f"Cannot send to {dst} (no route!)")  #만약 목적지가 본인 라우팅테이블에 없으면??? = 라우팅테이블 잘못 만든거지

    def on_start(self):
        self.send_vector_timer = 0