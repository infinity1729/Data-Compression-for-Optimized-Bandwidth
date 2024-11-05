from scapy.all import *
import numpy as np
import blosc

def compress_payload(payload):
    original_text = payload

    text = original_text.decode("ISO-8859-1")

    values = []
    for i in text:
        values.append(ord(i))

    val = np.array(values)
    original_data_bytes = val.tobytes()

    # Compress text and write to a file
    return blosc.compress(original_data_bytes)
    

def udp_packet_callback(packet):
    if packet.haslayer('Raw'):
        # print("\nSummary:\n")
        # print(packet.summary())
        # print("\nPayload:\n")
        # print(packet['Raw'].load)
        payload = packet['Raw'].load
        compressed_payload = compress_payload(payload)
        packet['Raw'].load = compressed_payload
        # print("\nCompressed Payload: \n")
        # print(packet['Raw'].load)
        # print()
        send(packet, iface="eth1")

        
# Replace 'eth0' with your specific Ethernet port
sniff(iface='eth0', filter='udp', prn=udp_packet_callback)
