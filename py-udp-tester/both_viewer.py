import socket
import struct

# local_ip = "127.0.0.1"
# local_port = 3000
my_ip = "192.168.10.151"
my_port = 2000
target_ip = "192.168.10.160"
target_port = 1000
buffersize = 1024

server_addr_port = (target_ip, target_port)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((my_ip, my_port))
UDPServerSocket.setblocking(False)
print("Server IP Addr : {}".format((my_ip, my_port)))
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

  # msg_from_client = b'\x70\x00\x70\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40'
  UDPClientSocket.sendto(msg, server_addr_port)
  # # Show raw message
  # print(msg)

  # # Show bytes as HEX
  # for i in range(len(msg)):
  #   print("{:02x}".format(msg[i]),end=' ')
  # print("")