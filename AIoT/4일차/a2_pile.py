import sys

from scapy.all import *
import socket

def select_iface():
    iface_list = socket.if_nameindex()

    if len(iface_list) == 0:
        print("No network interface found")
        sys.exit()

    print("Available network interfaces: ")
    for iface in iface_list:
        i, face = iface

        print(f"{i}: {face}")
    i = int(input(f"\nSelect interface number(1-{len(iface_list)}): "))

    return iface_list[i - 1][1]
    

def process_packet(file_name, packet):
    wrpcap(file_name, pkt=packet, append=True)


def main():
    # 저장할 이름​
    file_name = str(sys.argv[1])

    # 수집 기간 ( time )​
    duration = int(sys.argv[2])

    iface = select_iface()
    sniff(
        iface=iface,
        filter="tcp or udp or icmp",
        prn=lambda pkt: process_packet(file_name, pkt),
        timeout=duration,
    )

    print(f"\nPackets captured from {iface} for {duration}s")

if __name__ == "__main__":
    main()