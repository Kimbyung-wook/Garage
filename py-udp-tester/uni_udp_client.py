import socket
import struct

msg_list = []; 
msg_list.append({'name':'id'    , 'type':'b', 'value': 61})
msg_list.append({'name':'int'   , 'type':'i', 'value': 12345})
msg_list.append({'name':'double', 'type':'d', 'value': 37.1234567})
msg_list.append({'name':'float' , 'type':'f', 'value': 126.1234567})

# local_ip = "127.0.0.1"
local_ip = "192.168.10.61"
local_port = 5252
server_addr_port = (local_ip, local_port) 
msg_from_client = bytearray()
for i in range(len(msg_list)):
  msg_list[i]['value']

  bytearr = bytearray(struct.pack(msg_list[i]['type'],msg_list[i]['value']))
  print("{} : {} -> {} : {}".format(msg_list[i]['name'], msg_list[i]['value'], len(bytearr), bytearr))
  msg_from_client = msg_from_client + bytearr
  print("msg {} : {}".format(len(msg_from_client),msg_from_client))

print("Send to ", server_addr_port)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(msg_from_client, server_addr_port)
print(msg_from_client)