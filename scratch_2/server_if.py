# implementing 3-tier structure: Hall --> Room --> Clients; 

import select, socket, sys, pdb
from backend import Hall, Room, Player
import backend
from time import sleep

READ_BUFFER = 4096
stored_exception=None


print ('script started')

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = backend.create_socket((host, backend.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    # Player.fileno()
    # print('starting while loop')
    
    if stored_exception:
        print('caught exception: Keyboard Interrupt')
        break
    
    try:
        print('reached here')
        read_players, write_players, error_sockets = select.select(connection_list, [], [])
        for player in read_players:
            if player is listen_sock: # new connection, player is a socket
                new_socket, add = player.accept()
                new_player = Player(new_socket)
                connection_list.append(new_player)
                hall.welcome_new(new_player)
    
            else: # new message
                msg = player.socket.recv(READ_BUFFER)
                #print(msg) # debug
                if msg:
                    msg = msg.decode().lower()
                    #print(msg) # debug
                    #print('*****')
                    # hall.handle_msg(player, msg)
                else:
                    player.socket.close()
                    connection_list.remove(player)
    
        for sock in error_sockets: # close error sockets
            sock.close()
            connection_list.remove(sock)

    except KeyboardInterrupt:
        stored_exception=sys.exc_info()
        
# clean up
print(connection_list)
for player in connection_list:
    player.socket.close()
    print('Connection Closed to:')
    print(player)
    
