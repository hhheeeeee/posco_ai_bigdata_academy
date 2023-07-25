from router_lab import NodeCustomBase


class DummyNodeImpl(NodeCustomBase):
    # NOTE : all functions are optional

    async def every_1s(self): #1초마나 한번씩 무조건 실행되는 함수, 데이터를 보내거나 할 때 쓰면 좋겟져?
        pass

    async def main(self): #시뮬레이션 시작하고 노드에서 뭐가 실행되는지
        await self.broadcast(b"Hello, world!") # 모든 노드에 바이트 단위로 변환함 'hellow,world'를 보내용

    async def on_recv(self, src_1hop: str, data: bytes): #패킷이 다른데로부터 왓으면 , 실행이 된다. 
        self.log.info(f"Received from {src_1hop}: {data}") # 그 패킷의 목적지가 나일수도, 아님 목적지가 다른데인데 나를 거쳐갈 수도 잇다. 
        if data == b"Hello, world!":  
            await self.unicast(src_1hop, b"Hello, " + src_1hop.encode() + b"!") #패킷을 받았을 때 어디로 보낼지 그걸 내 라우팅테이블에 따라서 보내야 된다

    async def on_queue(self, dst: str, data: bytes): # 시뮬레이터에서 노트 패킷 ENQUEUE RATE 결정하고 생성이 되면 이 함수가 실행이 된다. 
        pass  #DEST는 IP 내 노드에서 패킷이 생성되면 보애야되니까 , 어디로 보낼건지, 뭘 보낼건지
    # 본인이 생성한 패키지를 어디로 보낼지를 정해주는 함수


    # NOTE : on_start is synchronous (not async)
    def on_start(self):    #노드 시작 전에 실행되는거, 그냥 로그 보여주는 용도임
        self.log.info(f"Node started (${self.ip})")

    # NOTE : on_stop is synchronous (not async)
    def on_stop(self):  #실행 후에 실행되는거 그냥 로그 보여주는 용도임
        self.log.info(f"Node stopped (${self.ip})")
