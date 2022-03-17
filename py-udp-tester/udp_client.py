import socket

# 클라이언트가 보내고자 하는 서버의 IP와 PORT
server_ip = "127.0.0.1"
server_port = 3000
server_addr_port = (server_ip, server_port)

# 보낼 메시지를 byte 배열로 바꾼다.
msg_from_client = "Hello Server from client"
bytes_to_send = str.encode(msg_from_client)

# 소켓을 UDP로 열고 서버의 IP/PORT로 메시지를 보낸다.
udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_client_socket.sendto(bytes_to_send, server_addr_port)
