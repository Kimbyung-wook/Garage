import socket

msg_from_client = "Hello Server"
server_addr_port = ("127.0.0.1", 3000)
bytes2send = str.encode(msg_from_client)
buffer_size = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytes2send, server_addr_port)

# msg_from_server = UDPClientSocket.recvfrom(buffer_size)
# msg = "msg from server {}".format(msg_from_server[0])
# print(msg)