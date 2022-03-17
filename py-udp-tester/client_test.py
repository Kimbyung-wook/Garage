import socket

msg_from_client = b'\x70\x00\x70\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40'
server_addr_port = ("127.0.0.1", 3000)
# bytes2send = str.encode(msg_from_client)
buffer_size = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(msg_from_client, server_addr_port)

# msg_from_server = UDPClientSocket.recvfrom(buffer_size)
# msg = "msg from server {}".format(msg_from_server[0])
# print(msg)