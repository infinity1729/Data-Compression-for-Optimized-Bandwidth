from scapy.all import Ether, IP, TCP, sendp, send

def send_ethernet_packet(destination_mac, source_mac, payload):
    # Craft an Ethernet frame
    ethernet_frame = Ether(dst=destination_mac, src=source_mac) / payload

    # Send the packet
    sendp(ethernet_frame, verbose=True)

# Example usage
destination_mac = "36:b7:f8:78:e7:99"  # Replace with the actual destination MAC address
source_mac = "d2:54:49:90:18:1a"       # Replace with the actual source MAC address

# Craft an IP packet as payload (you can customize this part)
ip_packet = IP(src="192.168.1.4", dst="192.168.5.3") / TCP(dport=80, sport=1234)

send(ip_packet, verbose=True)
# exit()

# Send the Ethernet packet with the IP payload
send_ethernet_packet(source_mac, destination_mac, ip_packet)
