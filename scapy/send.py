from scapy.all import *

def send_file_in_chunks(file_path, source_ip, source_port, destination_ip, destination_port, chunk_size=1024):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            # Craft a UDP packet with the file chunk as payload
            packet = IP(src=source_ip, dst=destination_ip) / UDP(sport=source_port, dport=destination_port) / Raw(load=chunk)

            # Send the packet
            send(packet, iface="eth0")

# Example usage
file_path = './file.txt'
destination_ip = '192.168.12.25'
source_ip = '192.168.10.20'
destination_port = 12345
source_port = 12345

send_file_in_chunks(file_path, source_ip, source_port, destination_ip, destination_port)