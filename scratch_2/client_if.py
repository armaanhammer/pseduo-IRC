import select, socket, sys
from backend import Room, Hall, Player
import backend
from time import sleep

READ_BUFFER = 4096

if len(sys.argv) < 2:
    print("Usage: Python3 client.py [hostname]", file = sys.stderr)
    sys.exit(1)
else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection.connect((sys.argv[1], backend.PORT))

def prompt():
    print('>', end=' ', flush = True)
    #print('got here')

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    #sleep(1)
    #print('starting loop')
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        #print('sockets') # debug
        #print(s)
        if s is server_connection: # incoming message 
            #print('server connection') # debug
            #print(s)
            msg = s.recv(READ_BUFFER)
            #print(msg) #debug
            if not msg:
                print("Server down!")
                sys.exit(2)
            else:
                if msg == backend.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                if 'Please tell us your name' in msg.decode():
                    msg_prefix = 'name: ' # identifier for name
                else:
                    msg_prefix = ''
                prompt()

        else:
            #print('*****reached ELSE')
            #print(msg_prefix)
            msg = msg_prefix + sys.stdin.readline()
            #print(msg)
            server_connection.sendall(msg.encode())
            #msg = ''
            #print(msg)
			#print(READ_BUFFER)
