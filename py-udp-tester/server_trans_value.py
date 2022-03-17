import socket
import struct

local_ip = "127.0.0.1"
local_port = 3000
# local_ip = "192.168.10.151"
# local_port = 2000
buffersize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((local_ip, local_port))
UDPServerSocket.setblocking(False)
print("Server IP Addr : {}".format((local_ip, local_port)))
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

  # print(msg)
  # msg_types = {'H', 'B', 'd', 'd'}
  # for i in range(len(msg_types))
  id = struct.unpack('H',msg[0:2])[0] # ushort
  check = struct.unpack('B',msg[2:3])[0] # uchar
  value1 = struct.unpack('d',msg[3:11])[0] # double
  value2 = struct.unpack('d',msg[11:19])[0] # double
  print("msg : {} {} {} {}".format(id,check,value1,value2))

  for i in range(len(msg)):
    print("{:02x}".format(msg[i]),end=' ')
  print("")