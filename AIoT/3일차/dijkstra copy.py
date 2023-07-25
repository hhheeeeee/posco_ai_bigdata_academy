import time

from router_lab import NodeCustomBase, is_valid_ip


class DijkstraRoutingPacket:
    def __init__(self, src: str,link_states: dict[str, float]):
        self.src = src
        self.link_states: dict[str, float] = link_states
# DijkstraRoutingPacket 클래스는 Dijkstra 알고리즘을 사용하여 라우팅 테이블 정보를 전송하기 
# 위한 패킷을 나타냅니다. src는 패킷의 출발지 IP 주소이고, link_states는 
# 이웃 노드들과의 연결 상태 및 비용 정보를 나타내는 딕셔너리입니다.

    # 정보를 바이트로
    def to_bytes(self) -> bytes:
        return (
            b"routing\n"
            + self.src.encode()
            + b"\n"
            + b"\n".join(f"{dst} {cost}".encode() for dst, cost in self.link_states.items())
        )

# to_bytes 메서드는 객체를 바이트로 변환하여 네트워크를 통해 전송할 수 있는 형태로 만듭니다. 
# 출발지 IP 주소와 link_states의 항목을 바이트로 변환한 후, 
# 줄 바꿈 문자로 구분하여 연결 상태 및 비용 정보를 추가합니다.



    # 바이트로 된 정보들을 line에 저장
    @classmethod
    def from_bytes(cls, data: bytes) -> "DijkstraRoutingPacket":
        lines = data.split(b"\n")
        src = lines[1].decode()
        link_states = {}
        for line in lines[2:]:
            if not line:
                continue
            dst, cost = line.decode().split()
            # error handling error로 생성된 이상한 ip가 없도록
            assert is_valid_ip(dst), "Invalid IP, maybe bit corruption!"
            link_states[dst] = float(cost)
        return cls(src,link_states)
# from_bytes 메서드는 바이트로 된 패킷 데이터를 받아 DijkstraRoutingPacket 객체로 변환합니다.
#  줄 바꿈 문자를 기준으로 데이터를 분리하고, 
# 출발지 IP 주소와 연결 상태 및 비용 정보를 추출하여 객체를 생성합니다.


class DataPacket:
    def __init__(self, src: str, dst: str, hop: int, data: bytes):
        self.src = src
        self.dst = dst
        self.hop = hop
        self.data = data
# DataPacket 클래스는 데이터를 전송하기 위한 패킷을 나타냅니다. 
# src는 패킷의 출발지 IP 주소, dst는 목적지 IP 주소, 
# hop은 패킷이 전달된 노드의 수, data는 전달되는 실제 데이터입니다.
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
# to_bytes 메서드는 DataPacket 객체를 바이트로 변환합니다. 
# 객체의 정보를 바이트로 변환한 후, 줄 바꿈 문자로 구분하여 연결합니다.
    @classmethod
    def from_bytes(cls, data: bytes) -> "DataPacket":
        lines = data.split(b"\n")
        src = lines[1].decode()
        dst = lines[2].decode()
        hop = int(lines[3].decode())
        data = lines[4]
        return cls(src, dst, hop, data)

# from_bytes 메서드는 바이트로 된 패킷 데이터를 받아 NullPacket 객체로 변환합니다. 
# 줄 바꿈 문자를 기준으로 데이터를 분리하고, 
# 객체의 필드에 해당하는 정보를 추출하여 객체를 생성합니다.

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

class DijkstraNodeImpl(NodeCustomBase):
    def run_dijkstra(self):
        self.log.info(f"all_link_states ({len(self.all_link_states)}) = {self.all_link_states}")

        D: dict[str, float] = {}
        S: set[str] = set()
        S.add(self.ip)
        for node_ip in self.all_link_states:
                if node_ip in self.my_link_states:
                    D[node_ip] = self.my_link_states[node_ip]
                else:
                    D[node_ip] = float("inf")
        D[self.ip] = 0
        p: dict[str, str] = {self.ip: self.ip}

        for node in self.my_link_states:
            p[node] = node

        while len(S) < len(self.all_link_states):
            min_node = None
            min_cost = float("inf")
            for node_ip in D:
                if node_ip not in S and D[node_ip] < min_cost:
                    min_node = node_ip
                    min_cost = D[node_ip]
            assert min_node is not None, "Graph is not connected!"
            S.add(min_node)
            for node_ip in self.all_link_states[min_node]:
                if node_ip not in S:
                    if(D[min_node] + self.all_link_states[min_node][node_ip]) < D[node_ip]:
                        D[node_ip] = D[min_node] + self.all_link_states[min_node][node_ip]
                        p[node_ip] = min_node
        self.routing_table = {}
        for node_ip in self.all_link_states:
            if node_ip != self.ip:
                self.routing_table[node_ip] = (p[node_ip], D[node_ip])
                self.record_table(node_ip, next_hop=p[node_ip], cost=D[node_ip])

        self.log.info("Computed Dijkstra's routing table!")

# DijkstraNodeImpl 클래스는 NodeCustomBase 클래스를 상속하여 Dijkstra 알고리즘을 
# 구현한 노드를 나타냅니다. run_dijkstra 메서드는 Dijkstra 알고리즘을 실행하여 현재 노드의 
# 라우팅 테이블을 계산합니다. 
# 이 알고리즘은 노드의 링크 상태와 비용을 사용하여 최단 경로를 계산합니다.

    async def every_1s(self):
        self.timer += 1
        if self.timer > 10 and not self.is_self_flooded:
            self.is_self_flooded = True
            self.flooding_check.append(self.ip)
            self.all_link_states[self.ip] = self.my_link_states.copy()
            await self.broadcast(DijkstraRoutingPacket(self.ip, self.my_link_states).to_bytes())
        if self.timer > 40 and not self.is_routing_table_calculated:
            self.is_routing_table_calculated = True
            self.run_dijkstra()
# every_1s 메서드는 1초마다 호출되는 메서드로, 노드의 타이머를 증가시키고 일정 시간 이후에 
# 자가 플러딩(self-flooding) 및 라우팅 테이블 계산을 수행합니다. 
# 자가 플러딩은 노드가 자신의 링크 상태를 다른 노드들에게 알리기 위해 패킷을 브로드캐스트합니다.
#  라우팅 테이블 계산은 Dijkstra 알고리즘을 실행하여 최단 경로를 계산하고 라우팅 테이블을 업데이트합니다.
    async def main(self):
        self.timer = 0
        self.is_self_flooded = False
        self.is_routing_table_calculated = False
        self.routing_table: dict[str, tuple[str, float]] = {}
        self.my_link_states: dict[str, float] = {}
        self.all_link_states: dict[str, dict[str, float]] = {}
        self.flooding_check: list[str] = []
        await self.broadcast(NullPacket(False, time.time()).to_bytes())
# main 메서드는 노드의 메인 루프로, 노드가 실행되는 동안 지속적으로 실행됩니다. 
# 노드의 초기 설정을 초기화하고, 
# 1초마다 every_1s 메서드를 실행하여 자가 플러딩 및 라우팅 테이블 계산을 수행

    async def on_recv(self, src: str, pkt_bytes: bytes):
        if pkt_bytes.startswith(b"routing"):
            pkt = DijkstraRoutingPacket.from_bytes(pkt_bytes)
            if pkt.src not in self.flooding_check:
                self.log.info(f"Received routing table from {src}: {pkt.link_states}")
                self.all_link_states[pkt.src] = pkt.link_states
                self.flooding_check.append(pkt.src)
                await self.broadcast(pkt_bytes)
            elif pkt_bytes.startswith(b"data"):
                pkt = DataPacket.from_bytes(pkt_bytes)
                if pkt.dst == self.ip:
                    self.log.info(f"Received from {pkt.src} with {pkt.hop} hops: {pkt.data}")
                    self.record_stat(routed_hops=pkt.hop)
                else:
                    next_hop, cost = self.routing_table[pkt.dst]
                    self.log.info(f"Sending to {pkt.dst} via {next_hop} (cost : {cost})")
                    await self.unicast(
                        next_hop, DataPacket(self.ip, pkt.dst, pkt.hop +1, pkt.data).to_bytes()
                    )
            elif pkt_bytes.startswith(b"null"):
                pkt = NullPacket.from_bytes(pkt_bytes)
                if pkt.is_ack:
                    self.my_link_states[src] = time.time() - pkt.timestamp
                else:
                    await self.unicast(src, NullPacket(True, time.time()).to_bytes())
            else:
                self.log.warning(f"Unknown packet from {src}!")
# recv 메서드를 사용하여 패킷을 수신하고,
#  수신된 패킷의 유형에 따라 적절한 동작을 수행합니다. 
# DijkstraRoutingPacket을 수신하면 자가 플러딩을 수행하고,
#  DataPacket을 수신하면 라우팅 테이블을 참조하여 패킷을 전달합니다.
#  NullPacket을 수신하면 ACK를 확인하거나 NULL을 수신한 타임스탬프를 기록합니다.

        async def on_queue(self, dst: str, data: bytes):
            if dst in self.routing_table:
                next_hop, cost = self.routing_table[dst]
                self.log.info(f"Sending to {dst} via {next_hop} (cost : {cost})")
                await self.unicast(next_hop, DataPacket(self.ip, dst, 1, data).to_bytes())
            else:
                self.log.info(f"Cannot send to {dst} (no route!)")