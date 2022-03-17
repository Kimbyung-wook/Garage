import socket

# local_ip = "127.0.0.1"
# local_port = 3000
local_ip = "192.168.10.160"
local_port = 1000
msg_from_client = b'\x70\x00\x70\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40'
server_addr_port = (local_ip, local_port)
# bytes2send = str.encode(msg_from_client)
buffer_size = 1024

print("Send to ", server_addr_port)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(msg_from_client, server_addr_port)