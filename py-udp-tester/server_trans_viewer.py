import socket
import struct

# local_ip = "127.0.0.1"
# local_port = 3000
local_ip = "192.168.10.151"
local_port = 2000
buffersize = 1024

msg_from_server = "Hello Client"
bytes2send = str.encode(msg_from_server)

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

  msg  = byte_addr_pair[0]
  addr = byte_addr_pair[1]  # Sender IP/Port

  msg_types = ['H', 'B', 'd', 'd']
  msg_value = []
  idx = 0
  data_size = 0
  for i in range(len(msg_types)):
    if (msg_types[i] == 'b' or msg_types[i] == 'B'):
      data_size = 1
    elif (msg_types[i] == 'h' or msg_types[i] == 'H'):
      data_size = 2
    elif (msg_types[i] == 'i' or msg_types[i] == 'I'):
      data_size = 4
    elif (msg_types[i] == 'f'):
      data_size = 4
    elif (msg_types[i] == 'd'):
      data_size = 8
    # print(data_size, msg_types[i])
    msg_value.append(struct.unpack(msg_types[i], msg[idx:(idx+data_size)])[0])
    idx = idx + data_size

  # Show parsed value
  for i in range(len(msg_value)):
    print("{} ".format(msg_value[i]), end='')
  print("")

  # # Show raw message
  # print(msg)

  # # Show bytes as HEX
  # for i in range(len(msg)):
  #   print("{:02x}".format(msg[i]),end=' ')
  # print("")