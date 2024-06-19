from scapy.all import IPv6, ICMP, send, Raw

context_id = 40
# Construct an IPv6 packet with an ICMPv6 payload
ipv6_packet = IPv6(src="2001:db8::1", dst="2001:db8::2")
ipv6_packet.add_payload(Raw(load=f"context:{context_id}"))
print(ipv6_packet.payload.load)
print(ipv6_packet.version)
# Send the packet
# ipv6_packet.show()
# print(type(ipv6_packet))