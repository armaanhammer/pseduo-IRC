# CS 594 Spring 2018
#
# Armaan Roshani
# pseudo-IRC server/client
#
# IRC_server_if.py
# Internet Relay Chat - Server Interface

import select, socket, sys, pdb
from IRC_backend import Hall, Room, User
import IRC_backend

READ_BUFFER = 4096

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = IRC_backend.create_socket((host, IRC_backend.PORT))

hall = Hall()
#connection_list = []
#connection_list.append(listen_sock)
hall.connection_list.append(listen_sock)

while True:
    # User.fileno()
    read_users, write_users, error_sockets = select.select(hall.connection_list, [], [])
    for user in read_users:
        if user is listen_sock: # new connection, user is a socket
            new_socket, add = user.accept()
            new_user = User(new_socket)

            # prototype code
            #hall.connection_dict[new_user.name]


            hall.connection_list.append(new_user)
            hall.welcome_new(new_user)

        else: # new message
            msg = user.socket.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(user, msg)
            else:
                user.socket.close()
                hall.connection_list.remove(user)

    for sock in error_sockets: # close error sockets
        sock.close()
        hall.connection_list.remove(sock)
