import socket
import struct
import argparse
from msg_list import msg_list

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Parse data from FCM via UDP')
  parser.add_argument('-p', help="My Port", required=False, default=5252)

  args = parser.parse_args()
  server_ip   = socket.gethostbyname(socket.gethostname())
  server_port = int(args.p);
  server_addr_port = (server_ip, server_port)

  udp_from_fcm = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  udp_from_fcm.bind(server_addr_port)
  udp_from_fcm.setblocking(False)
  print("Server IP Addr : {}".format(server_addr_port))
  # udp_from_fcm.settimeout(1.0)

  print("UDP server up and listening")

  # Listen Datagram incoming
  while(True):
    try:
      byte_addr_pair = udp_from_fcm.recvfrom(1024)
    except BlockingIOError:
      continue

    msg  = byte_addr_pair[0]
    addr = byte_addr_pair[1]  # Sender IP/Port

    # Parse message
    states = {}
    idx = 0
    data_size = 0
    for i in range(len(msg_list)):
      if (msg_list[i]['type'] == 'b' or msg_list[i]['type'] == 'B'):
        data_size = 1
      elif (msg_list[i]['type'] == 'h' or msg_list[i]['type'] == 'H'):
        data_size = 2
      elif (msg_list[i]['type'] == 'i' or msg_list[i]['type'] == 'I'):
        data_size = 4
      elif (msg_list[i]['type'] == 'f'):
        data_size = 4
      elif (msg_list[i]['type'] == 'd'):
        data_size = 8
      # print(data_size, msg_list[i])
      value = struct.unpack(msg_list[i]['type'], msg[idx:(idx+data_size)])[0]
      states[msg_list[i]['name']] = value
      idx = idx + data_size

    print("id {} int {} double {} float {}".format(states['id'], states['int'], states['double'], states['float']))