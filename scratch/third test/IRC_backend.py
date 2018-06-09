# implementing 3-tier structure: Hall --> Room --> Clients; 

import socket, pdb

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'

instructions = b'-------------------------\n'\
    + b'Instructions:\n'\
        + b'/rooms - lists all rooms on server\n'\
            + b'/list - lists all users on server\n'\
            + b'/list [room name] - lists all users in a specific room\n'\
            + b'/join [room_name] - joins a room. If the room does not exist yet,\n' \
            + b'\t it will be created.\n' \
            + b'/switch [room name] - switch which room you broadcast to\n' \
            + b'/leave [room_name] - leaves a room.\n' \
            + b'/msg [user] - Private Messages a user.\n' \
            + b'/help - shows instructions\n' \
            + b'/quit - ends the session\n' \
            + b'-------------------------\n'


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s


class Hall:
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.users = {} # {userName: roomName}


    def welcome_new(self, new_user):
        new_user.socket.sendall(b'Welcome to IRC.\nPlease type your name:\n')


    def list_rooms(self, user):
        if len(self.rooms) == 0:
            msg = 'No active rooms. Create your own!\n' \
                + 'Use /join [room_name] to create a room.\n'
            user.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())


        def remove_user(self, user):
            if user.name in self.subscribed:
                self.rooms[self.subscribed[user.name]].remove_user(user)
                del self.subscribed[user.name]
                print("User: " + user.name + " has left\n")


	# meat of the server
	def handle_msg(self, from_user, msg):

    	split_msg = msg.split()
        if(0 == len(split_msg)): # bad things happened
            print('received a zero-length message!')


        print(from_user.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            from_user.name = name
            print("New connection from:", from_user.name)
            from_user.socket.sendall(instructions)


        elif split_msg[0] == "/rooms": # list rooms
            self.list_rooms(from_user)


        elif split_msg[0] == "/list": # list users
            if len(split_msg) == 1: # list all users
                msg = b'Users on server: '
                for user in self.users:
                    msg += user.name.encode() + b', '

            else: # list users in specified room
                room_name = split_msg[1]
                if room_name in self.rooms:
                    msg = self.rooms[room_name].list(from_user)

            from_user.socket.sendall(msg + b'\n')


        elif split_msg[0] == "/join" or "/switch": # join room
            if len(split_msg) >= 2: # error check
                room_name = split_msg[1]

                # switch to room already joined
                if (room_name in from_user.rooms) and (room_name in from_user.rooms):
                    from_user.socket.sendall(b'Broadcasting to: [' + room_name.encode() + b']')
                    from_user.current_room = room_name

                # join room already created
                    elif room_name in self.rooms:
                    self.rooms[room_name].users.append(from_user)
                    self.rooms[room_name].welcome_new(from_user)
                    from_user.rooms.append(room_name)
                    from_user.current_room = room_name

                else: # new room:
                    new_room = Room(room_name)
                    self.rooms[room_name] = new_room
                    self.rooms[room_name].users.append(from_user)
                    self.rooms[room_name].welcome_new(from_user)
                    from_user.rooms.append(room_name)
                    from_user.current_room = room_name

        	else:
            	user.socket.sendall(instructions)


            elif split_msg[0] == "/leave": # leave room
                if len(split_msg) >= 2: # error check
                    room_name = split_msg[1]

                    if (room_name in self.rooms) and (room_name in from_user.rooms):
                        self.rooms[room_name].remove_user(from_user)
                        if len(self.rooms[room_name].users) == 0:
                            self.rooms = self.delete_room(room_name) # WTF?
                        from_user.rooms.remove(room_name)
                        msg = b': You have left ' + room_name.encode() + b'\n'

                    elif not (room_name in self.rooms):
                        msg = b'Room [' + room_name.encode() + b'] does not exist.\n'

                    else:
                        msg = b'You never joined [' + room_name.encode() + b'].\n'

                    from_user.current_room = room_name

                else: msg = b'Usage: /leave [room_name]\n'

                from_user.socket.sendall(msg)


            elif split_msg[0] == "/help": # print instructions
                user.socket.sendall(instructions)


            elif split_msg[0] == "/quit": # end session
                user.socket.sendall(QUIT_STRING.encode())
                self.remove_user(user)


            elif split_msg[0] == "/msg": # private message another user
                if len(split_msg) >= 2: # error check
                    to_user = split_msg[1]
                    for target in self.users:
                        if to_user == target:
                            msg = b'<' + from_user.name.encode() + b'>: ' + \
                                    + msg.split(' ',2)[2].encode()
                            target.socket.sendall(msg)

                        else: # target user not on server
                            from_user.socket.sendall(b'User <' + to_user.encode() + b'> not found')
                else:
                    user.socket.sendall(instructions)


            # end condition: broadcast, or fail
            else:
                if from_user.current_room in self.rooms: # broadcast
                    self.rooms[from_user.current_room](from_user.name, msg)
            	else:
                    msg = 'You are currently not in any room! \n' \
                        + 'Use /rooms to see available rooms! \n' \
                        + 'Use /join [room_name] to join a room! \n'
                    user.socket.sendall(msg.encode())


class Room:
    def __init__(self, name):
        self.users = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_user):
        msg = self.name + b" welcomes: " + from_user.name + '\n'
        for user in self.users:
            user.socket.sendall(msg.encode())
    
    def broadcast(self, from_user, msg):
        msg = b'[' + self.name.encode() + b']' + from_user.name.encode() + b":" + msg
        for user in self.users:
            #if user != from_user:
            user.socket.sendall(msg)
    
    def list(self, from_user):
        if len(self.users) > 0:
            msg = b'Users in [' + self.name.encode() + b']:'
                for user in self.users:
                    msg += user.name.encode() + b', '
                        else:
                            msg = b'No users in this room.'

                                # from_user.socket.sendall(msg + b'\n')
                                return msg

def remove_user(self, from_user):
    self.users.remove(from_user)
    leave_msg = b'[' + self.name.encode() + b']' + \
        from_user.name.encode() + b"has left the room\n"
        self.broadcast(from_user, leave_msg)


class User:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
            self.rooms = []
            self.current_room = ''

        def fileno(self):
                return self.socket.fileno()
