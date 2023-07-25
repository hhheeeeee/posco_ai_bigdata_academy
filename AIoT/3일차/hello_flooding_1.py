import uuid

from router_lab import NodeCustomBase

class SimpleFloodingPacket: #아이디는 패킷의 아이디임. 본인 패킷 고유 아이디를 가지고 있고 
    def __init__(self, id : str, src : str, dst : str, data : bytes):
        self.id = id
        self.src = src
        self.dst = dst
        self.data = data
    
    def to_bytes(self) -> bytes: #아이디랑 소스, 데스트 데이터를 바이트 형태로 저장하고 리턴한다
        return (
            b"flooding\n"
            + self.id.encode()
            + b"\n"
            + self.src.encode()
            + b"\n"
            + self.dst.encode()
            + b"\n"
            + self.data
        )
    
    @classmethod
    def from_bytes(cls, data : bytes) -> "SimpleFloodingPacket": # 바이트에서 정보들을 뽑아냄
        lines = data.split(b"\n")
        id = lines[1].decode()
        src = lines[2].decode()
        dst = lines[3].decode()
        data = lines[4]
        return cls(id, src, dst, data) #심플플러딩패킷 클래스를 리턴한다?
    
class HelloPacketNodeImpl(NodeCustomBase) :
    async def every_1s(self):
        self.timer += 1
        if self.timer % 20 == 1: # 20초마다 한번씩
            await self.broadcast( 
                SimpleFloodingPacket( #uuid는 본인..self는 소스의 ip, random은 시뮬레이션에 있는거 중에 랜덤 ip
                    str(uuid.uuid4())[:4], self.ip, self.get_random_ip(), b"Hello!"
                ).to_bytes()
            )
        
    async def main(self):
        self.timer = 0
        self.received_ids = set() #아무것도 안 들어가 잇는 set

    async def on_recv(self, src_1hop: str, data: bytes):
        pkt = SimpleFloodingPacket.from_bytes(data)
        if pkt.id in self.received_ids: 
            return #이미 받은 패킷이면 아무것도 안하고 리턴한다
        if pkt.dst == self.ip: #만약 패킷의 목적지가 본인이다. 그러면 내가 패킷을 받았다라는 로그를 띄워준다
            self.log.info(f"I'm {self.ip}, and received from {pkt.src}: {pkt.data}")
            self.received_ids.add(pkt.id) #받았으니까 receivedids에 저장하고 나중에 또 왔을 때는 그냥 아무것도 하지 말고 리턴하게, 
            if pkt.data == b"Hello!":
                await self.broadcast( 
                    SimpleFloodingPacket(
                        str(uuid.uuid4())[:4],
                        self.ip,
                        pkt.src,  #이 패킷을 보낸 애
                        b"hello, " + pkt.src.encode() + b"!", #내가 잘 받앗다는걸 알려주고
                    )
                )
            
        else:
            self.received_ids.add(pkt.id)
            await self.broadcast(data) #목적지가 본인이 아니라 다른애면 그냥 목적지한테 갈 때까지 broadcast해준다