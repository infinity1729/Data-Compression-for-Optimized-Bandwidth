from scapy.all import IPv6, IP, TCP, send

class PacketProcessorScapy:
    context_mapping = {}
    def _init_(self):
        self.context_mapping = {}

    def process_uncompressed_packet(self, uncompressed_packet):
        data = uncompressed_packet[IP].payload.load.decode()
        result_array = data.split(', ')
        c_id = result_array[0]
        p_id = result_array[1]

        static_info = {}

        # Check if the packet is an IPv6 packet
        if IPv6 in uncompressed_packet and p_id == 10:
            ipv6_header = uncompressed_packet[IPv6]

            # Extract information from the IPv6 header
            static_info['src'] = ipv6_header.src
            static_info['dst'] = ipv6_header.dst
            static_info['version'] = ipv6_header.version
            static_info['nh'] = ipv6_header.nh
            static_info['fl'] = ipv6_header.fl

        self.context_mapping[(p_id, c_id)] = static_info


    def process_compressed_packet(self, compressed_packet):
        context_id = self.extract_context_id(compressed_packet)
        profile_id, static_info = self.packet_context.context_info[context_id]

        # Recreate the original header using static and dynamic information
        original_header = self.recreate_ipv6_packet(static_info, compressed_packet)
        return original_header

    # def extract_context_id(self, compressed_packet):
    #     pass

    # return Uncompressed or Compressed
    def isCompressedOrNot(self, packet):
        if IPv6 in packet:
            return 'Uncompressed'
        else:
            return 'Compressed'

    def recreate_ipv6_packet(self, compressed_packet):
        data = compressed_packet[IP].payload.load.decode()
        ipv6_payload = compressed_packet[IPv6].payload.load
        result_array = data.split(', ')
        c_id = result_array[0]
        p_id = result_array[1]

        static_info = {}
        if (p_id, c_id) in self.context_mapping:
            static_info = self.context_mapping[(p_id, c_id)]
        new_ipv6_packet = IPv6(src=static_info['src'], dst=static_info['dst'], version=static_info['version'], nh=static_info['nh'], fl=static_info['fl'])
        new_ipv6_packet.add_payload(ipv6_payload)
        return new_ipv6_packet
    
    
    def orig(self, packet):
        doubt = self.isCompressedOrNot(packet)
        if doubt == 'Compressed':
            forwarding_packet = self.recreate_ipv6_packet(packet)
        elif doubt == 'Uncompressed':
            forwarding_packet = packet[IPv6]

        return forwarding_packet

# Example Usage
packet_processor_scapy = PacketProcessorScapy

static_info = {
    'src': '2001:db8::1',  # Replace with the actual source IPv6 address
    'dst': '2001:db8::2',  # Replace with the actual destination IPv6 address
    'version': 6,           # IPv6 version
    'nh': 17,               # Next Header (protocol number for the payload, e.g., UDP)
    'fl': 1234              # Flow Label
}

# packet_processor_scapy.context_mapping.
packet_processor_scapy.context_mapping[(10, 1)] = static_info

context_mapping = {}
context_mapping[(10,1)] = static_info
print(static_info)



# Example Usage
ipv4_sender = "192.168.1.1"
ipv4_receiver = "192.168.2.2"
ipv6_sender = "2001:db8::1"
ipv6_receiver = "2001:db8::2"

# Create an IPv6 packet
ipv6_packet = IPv6(src=ipv6_sender, dst=ipv6_receiver)
pid = 10
cid = 1
payload = f"p_id: {pid}, c_id: {cid}"
ipv6_packet.add_payload(payload.encode())

# new_packet = orig(ipv6_packet)

ipv6_packet.show()
# exit()

# Create an IPv4 packet and add the above IPv6 packet below the IPv4
ipv4_packet = IP(src=ipv4_sender, dst=ipv4_receiver)
res_packet = ipv4_packet / ipv6_packet
res_packet.show()

# Process the uncompressed packet
# packet_processor_scapy.process_uncompressed_packet(ipv4_packet)

