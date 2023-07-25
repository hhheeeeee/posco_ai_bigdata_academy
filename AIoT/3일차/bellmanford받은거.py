from collections import defaultdict
from typing import DefaultDict

from router_lab import NodeCustomBase, is_valid_ip

import time


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


class DistributedBellmanFordNodeImpl(NodeCustomBase):
    async def every_1s(self):
        # Log routing table
        for dst, (next_hop, cost) in self.routing_table.items():
            self.record_table(dst, next_hop=next_hop, cost=cost)

        # Send distance vector for 20s
        if 10 <= self.send_vector_timer < 30:
            await self.broadcast(
                DBFRoutingPacket(
                    self.ip, {dst: cost for dst, (next_hop, cost) in self.routing_table.items()}
                ).to_bytes()
            )
        elif self.send_vector_timer < 10:
            await self.broadcast(NullPacket(False, time.time()).to_bytes())
        self.send_vector_timer += 1

    async def main(self):
        self.routing_table: DefaultDict[str, tuple[str, float]] = defaultdict(
            lambda: ("", float("inf"))
        )
        self.routing_table[self.ip] = (self.ip, 0.0)
        self.adjacent_delay: dict[str, float] = {}
        await self.broadcast(NullPacket(False, time.time()).to_bytes())

    async def on_recv(self, src_1hop: str, data: bytes):
        if data.startswith(b"routing"):
            pkt = DBFRoutingPacket.from_bytes(data)
            if pkt.src not in self.routing_table:
                self.routing_table[pkt.src] = (src_1hop, self.adjacent_delay[src_1hop])
            for dst, cost in pkt.routing_table.items():
                if (
                    dst not in self.routing_table
                    or self.routing_table[dst][1] > cost + self.adjacent_delay[src_1hop]
                ):
                    self.routing_table[dst] = (src_1hop, cost + self.adjacent_delay[src_1hop])
        elif data.startswith(b"data"):
            pkt = DataPacket.from_bytes(data)
            if pkt.dst == self.ip:
                self.log.info(f"Received from {pkt.src} with {pkt.hop} hops: {pkt.data}")
                self.record_stat(routed_hops=pkt.hop)
            else:
                next_hop, cost = self.routing_table[pkt.dst]
                self.log.info(f"Sending to {pkt.dst} via {next_hop} (cost: {cost})")
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
            self.log.warning(f"Unknown packet from {src_1hop}!")

    async def on_queue(self, dst: str, data: bytes):
        if dst in self.routing_table:
            next_hop, cost = self.routing_table[dst]
            self.log.info(f"Sending to {dst} via {next_hop} (cost: {cost})")
            await self.unicast(next_hop, DataPacket(self.ip, dst, 1, data).to_bytes())
        else:
            self.log.info(f"Cannot send to {dst} (no route!)")

    def on_start(self):
        self.send_vector_timer = 0
