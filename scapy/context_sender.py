from scapy.all import IP, IPv6

class PacketContextScapy:
    tunnel_dest_ipv4 = "10.0.0.1"
    context_counter = 1
    ipv4_interface = "10.0.0.3"

    def __init__(self):
        self.context_info = {}

    def increment_context(self):
        self.context_counter += 1
    
    def store_context(self, packet):
        static_info = self.extract_static_info(packet)
        context_id = self.context_counter
        profile_id = self.determine_profile_id(packet)
        self.context_info[static_info] = (profile_id, context_id)

    def extract_static_info(self, packet):
        # Extract static fields from the IPv6 packet
        s = f"{packet[IPv6].src}, {packet[IPv6].dst}, {packet[IPv6].nh}, {packet[IPv6].version}, {packet[IPv6].fl}"
        return s
    
    def determine_profile_id(self, packet):
        if IPv6 in packet:
            return 10
        else:
            return 20  # Return a different profile ID for non-IPv6 packets
    
    def create_new_packet(self, packet):
        if IPv6 in packet:
            new_ipv4_packet = IP(src=self.ipv4_interface, dst=self.tunnel_dest_ipv4)
            new_ipv4_packet.add_payload(f"c_id: {self.context_counter}, p_id: {self.determine_profile_id(packet)}, tc: {packet[IPv6].tc}, hlim: {packet[IPv6].hlim}, payload: {packet[IPv6].payload.load.decode('utf-8')}")
            return new_ipv4_packet
        else:
            return IP()  # Return a default IP packet for non-IPv6 packets
        
    # returns IPv4 packet
    def orig(self, packet):      
        self.store_context(packet)
        return self.create_new_packet(packet)


# Example Usage
sender_ipv6 = "2001:db8::1"
receiver_ipv6 = "2001:db8::2"
ipv6_packet = IPv6(src=sender_ipv6, dst=receiver_ipv6)
ipv6_packet.add_payload("hello world")
ipv6_packet.show()
# print(ipv6_packet)

# exit()

print('---------------------------------------')
packet_context_scapy = PacketContextScapy()
packet = packet_context_scapy.orig(ipv6_packet) / ipv6_packet
print (packet[IP].payload.load.decode('utf-8'))


# print(packet_context_scapy.context_info)
# print(packet_context_scapy.create_new_packet(ipv6_packet))
