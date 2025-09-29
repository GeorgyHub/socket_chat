from scapy.all import IP, ICMP, sr1

def ping(host):
    packet = IP(dst=host) / ICMP()
    response = sr1(packet, timeout=2)
    if response:
        print(f'{host} is up')
    else:
        print(f'{host} is down')

print('8.8.8.8')