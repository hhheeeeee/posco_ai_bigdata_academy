from scapy.all import *
import socket
import sys


def select_iface():  # 사용 가능한 네트워크 인터페이스 목록을 가져옴
    iface_list = socket.if_nameindex()

    if len(iface_list) == 0:  # 사용 가능한 네트워크 인터페이스를 찾을 수 없다면 종료
        print("NO network interfaces found")
        sys.exit()

    print("Available network interfaces:")

    for iface in iface_list:  # 사용 가능한 네트워크 인터페이스를 하나씩 출력
        i, face = iface
        print(f"{i}: {face}")

    i = int(input(f"\nSelect network interface number to capture [1-{len(iface_list)}]: "))
    # 네트워크 인터페이스의 인덱스 입력받음

    return iface_list[i - 1][1]  # 선택한 인터페이스의 이름을 반환


def process_packet(file_name, packet):
    wrpcap(filename=file_name, pkt=packet, append=True)  # 패킷을 지정된 파일에 추가하여 저장


def main():
    file_name = str(sys.argv[1])  # 저장한 파일의 이름을 가져옴
    duration = int(sys.argv[2])  # 캡처 시간을 가져옴

    iface = select_iface()  # 캡처할 네트워크 인터페아스룰 선택

    sniff(
        iface=iface,  # 선택한 인터페이스를 사용하여 패킷을 캡처
        filter="tcp or udp or icmp",  # TCP, UDP, ICMP 패킷만 필터링
        prn=lambda pkt: process_packet(file_name, pkt),  # 패킷이 캡처될 때 함수 호출
        timeout=duration,  # 캡처할 시간
    )

    print(f"\n Packets captured from {iface} for {duration}s and savsd to {file_name}")  # 캠처 정보 출력


if __name__ == "__main__":
    main()  # 메인 함수를 호출해 프로그램을 실행
