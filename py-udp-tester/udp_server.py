import socket

local_ip = "127.0.0.1"
local_port = 3000
buffersize = 1024

msg_from_server = "Hello Client"
bytes2send = str.encode(msg_from_server)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((local_ip, local_port))
UDPServerSocket.setblocking(False)
# UDPServerSocket.settimeout(1.0)

print("UDP server up and listening")

# Listen Datagram incoming
while(True):
  try:
    byte_addr_pair = UDPServerSocket.recvfrom(buffersize)
  except BlockingIOError:
    continue
  msg = byte_addr_pair[0]
  addr = byte_addr_pair[1]

  client_msg = "msg from client : {}".format(buffersize)
  client_ip  = "client IP Addr : {}".format(addr)

  print(client_msg)
  print(client_ip)
  print(msg)
  for i in range(len(msg)):
    print("{:02x}".format(msg[i]),end=' ')
  print("")
  # print(type(msg))
  # print(msg[0])
  # print(len(msg))

  # UDPServerSocket.sendto(bytes2send, addr)