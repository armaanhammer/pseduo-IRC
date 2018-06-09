# -*- coding: utf-8 -*-

# simple illustration client/server pair; client program sends a string
# to server, which echoes it back to the client (in multiple copies),
# and the latter prints to the screen

# this is the client

import argparse
import socket
import sys

def get_args():
    parser = argparse.ArgumentParser(description='IRC_server.')

    parser.add_argument(
            '--host',
            default='127.0.0.1',
            help='host ip of the IRC_server')

    parser.add_argument(
            '--port',
            default=5000,
            type=int,
            help='port used to communicate to the IRC_server')

    parser.add_argument(
            '-c',
            '--config_file',
            default='config_client.yaml',
            help='IRC_client configuration file')

    return parser.parse_args()

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print (sys.argv[0])

# connect to server
host = sys.argv[1] # server address
port = int(sys.argv[2]) # server port
s.connect((host, port))

x = 5

while(x>0):
  z = input()
  print (z)
  
  s.sendall(bytes(z, 'utf8')) # send test string
  #s.sendall(bytes(sys.argv[3], 'utf8')) # send test string
  
  print ('got here')
  print (sys.argv[3].encode)
  
  data = s.recv(100000)
  print (data)
  
# =============================================================================
#   # read echo
#   i = 0
#   while(1):
#     data = s.recv(1000000) # read up to 1000000 bytes
#     i += 1
#     if (i < 5):
#         print (data)
#     if not data: # if end of data, leave loop
#       break
#   print ('received', len(data), 'bytes')
# =============================================================================
  x = x-1

# close the connection
s.close()