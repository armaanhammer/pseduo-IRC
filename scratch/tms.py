# -*- coding: utf-8 -*-

# simple illustration client/server pair; client program sends a string
# to server, which echoes it back to the client (in multiple copies),
# and the latter prints to the screen

# this is the server

import argparse
import socket
import sys

print ('script started')
stored_exception=None

def get_args():
    parser = argparse.ArgumentParser(description='IRC_server.')

    parser.add_argument(
            '--host',
            default='192.168.0.108',
            help='host ip of the IRC_server')

    parser.add_argument(
            '--port',
            default=5000,
            type=int,
            help='port used to communicate to the IRC_server')

    parser.add_argument(
            '-c',
            '--config_file',
            default='config_server.yaml',
            help='IRC_server configuration file')

    return parser.parse_args()

# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# associate the socket with a port
host = '' # can leave this blank on the server side
port = int(sys.argv[1])
s.bind((host, port))

# accept "call" from client
s.listen(1)
conn, addr = s.accept()
print ('client is at', addr)

# read string from client (assumed here to be so short that one call to
# recv() is enough), and make multiple copies (to show the need for the
# "while" loop on the client side)


chars_to_send = 1 # meaning True for initial case
# while terminates when no more characters received
while(chars_to_send):
  print('starting while loop')

  if stored_exception:
    print('caught exception: Keyboard Interrupt')
    break
    
  try:
    data = conn.recv(1000000)
    print (data.decode("utf-8"))

# wait for the go-ahead signal from the keyboard (shows that recv() at
# the client will block until server sends)
# z = input()

# now send
    chars_to_send = conn.send(data)
    # print('chars_to_send')
    # print(chars_to_send)
    
  except KeyboardInterrupt:
    stored_exception=sys.exc_info()
    
# =============================================================================
#   data = conn.recv(1000000)
#   print (data.decode("utf-8"))
#   conn.send(data)
#   print ('sent data')
# =============================================================================
  

# close the connection
conn.close()
print('Connection Closed')