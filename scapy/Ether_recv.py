from scapy.all import Ether, IP, TCP, sendp, sniff

def packet_callback(packet):
    if packet.haslayer(Ether) and packet.haslayer(IP) and packet.haslayer(TCP):
        # Extracting original TCP payload
        original_payload = packet[TCP].payload
        original_payload.show()

        # Modify the payload as needed
       # new_payload = b"Modified Payload: " + original_payload
       # print(new_payload)
       # print()

        # Creating a new TCP packet with the modified payload
        new_payload = "not hello"

        new_TCP_packet = TCP(sport=packet[TCP].sport, dport=packet[TCP].dport) / new_payload

        # Create a new IP packet with the modified TCP packet
        new_ip_packet = IP(src=packet[IP].dst, dst=packet[IP].src) / new_TCP_packet

        # Create a new Ethernet frame with the modified IP packet
        new_eth_packet = Ether(src=packet[Ether].dst, dst=packet[Ether].src) / new_ip_packet

        # Send the modified packet
        sendp(new_eth_packet, iface="eth1")

# Start sniffing on the specified interface
sniff( prn=packet_callback, store=0)




exit()

# below code works
# works for custom ip packets

from scapy.all import sniff, IP

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"IP Packet: Source IP - {ip_src}, Destination IP - {ip_dst}")

# Sniff IP packets on the eth0 interface
sniff(iface="eth0", prn=packet_callback, store=0)
