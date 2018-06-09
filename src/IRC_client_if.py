# CS 594 Spring 2018
#
# Armaan Roshani
# pseudo-IRC server/client
#
# IRC_client_if.py
# Internet Relay Chat - Client Interface

import select, socket, sys
from IRC_backend import Room, Hall, User
import IRC_backend

READ_BUFFER = 4096 # handled by backend now

# Require user to enter hostname as command line argument
if len(sys.argv) < 2:
    print("Usage: Python3 client.py [hostname]", file = sys.stderr)
    sys.exit(1)
else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection.connect((sys.argv[1], IRC_backend.PORT))

# Prompt once client is running -- simulates terminal
def prompt():
    print('>', end=' ', flush = True)

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    # Check for data from server
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: # incoming message
            msg = s.recv(READ_BUFFER) # put message into buffer
            if not msg: # if s.recv() returns error, close connection (fail gracefully)
                print("Server down!")
                sys.exit(2)
            else:
                # close connection if server commands
                if msg == IRC_backend.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    # print message from server
                    sys.stdout.write(msg.decode())

                    # edge case: first message. Prompt for username
                    if 'Please type your name' in msg.decode():
                        msg_prefix = 'name: ' # identifier for name
                        #print('sending prefix')
                    else:
                        msg_prefix = ''
                    
                    # simulate terminal
                    prompt()

        else:
            msg = msg_prefix + sys.stdin.readline() # add edge-case prefix
            server_connection.sendall(msg.encode()) # Send message from client
