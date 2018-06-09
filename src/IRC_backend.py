# CS 594 Spring 2018
#
# Armaan Roshani
# pseudo-IRC server/client
#
# IRC_backend.py
# Internet Relay Chat - Backend

import socket, pdb, time

MAX_CLIENTS = 30 # This number can be increased. (limited only by system performance.)
PORT = 22222 # port server listens to and clients initially connect to
QUIT_STRING = '<$quit$>' # string to command client close connection
#READ_BUFFER = 4096 # max size of message on clients or server

# These are instructions sent to client
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

# function to create initial listening socket
def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s

# HALL CLASS 
# server creates a single one.
# Each Hall Class contains multiple users and mutliple clients.
# Exists as class to functionality could be extended into the future (Allows
# for multiple virtual servers with their own sets of Users and Rooms to live 
# in one application.)
class Hall:
    def __init__(self):
        self.rooms = {} # dict of rooms and Room Objects
                        # {room_name: Room}
        self.users = [] # list of users
                        # [users per hall]
        self.connection_list = [] # list of sockets
                                  # [socket per user]
        self.connection_dict = {} # dict of names and sockets
                                  # {userName: roomName}

    # function to welcome new user
    def welcome_new(self, new_user):
        new_user.socket.sendall(b'Welcome to IRC.\nPlease type your name:\n')

    # function to list users
    # if provided no argument, lists all users on server
    # if provided one or more arguments, tries to match first argument to a room name
    # if finds match, lists all users in matching room
    # if finds no match, tells client room does not exist.
    # discards any additional arguments.
    def list_rooms(self, user):
        #print('DEBUG: printing list of rooms: ')
        #print(self.rooms)
        try:
            if len(self.rooms) == 0:
                msg = 'No active rooms. Create your own!\n' \
                + 'Use /join [room_name] to create a room.\n'
                #user.socket.sendall(msg.encode())
            else:
                msg = 'Listing current rooms...\n'
                for room in self.rooms:
                    msg += room + ": " + str(len(self.rooms[room].users)) + " user(s)\n"
            user.socket.sendall(msg.encode())
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print('\nwtf do I do now, Dave?')

            user.socket.sendall(b'\n') # placeholder

    # function to gracefully remove user from objects on server
    def remove_user(self, user):
        if user.name in self.connection_dict:
            del self.connection_dict[user.name]
        if user.name in self.users:
            self.users.remove(user.name)
        print("User: " + user.name + " has left\n")

    # function to gracefully remove room from objects on server
    def delete_room(self, room_name):
        print(self.connection_dict)
        for test_user in self.connection_dict:
            print(self.connection_dict[test_user].name)
            if room_name in self.connection_dict[test_user].rooms:
                print('ERROR: trying to delete a room that users still are subscribed to.')
                print(self.connection_dict[test_user].name)

                return # exit function because some user still suscribed to room
        
        if room_name in self.rooms:
            print('room_name is in self.rooms')
            print('removing room')
            del self.rooms[room_name] # remove room
        else:
            print('ERROR: room_name is NOT in self.rooms')
        print(self.rooms)
        #self.rooms.remove(room_name)

        return

    # HANDLE MESSAGE function
    # meat of the server
    # parses messages, routes data, creates and removes users and rooms
    def handle_msg(self, from_user, msg):
        
        # split message so it can be parsed
        split_msg = msg.split()
        #print(msg)
        #print(split_msg)
        if(0 == len(split_msg)): # bad things happened
            print('WARNING: received a zero-length message!\n')
            return

        # output message text to server for easy debugging
        print(from_user.name + " says: " + msg)
        

        # detect user trying to name themselves
        if "name:" in msg:
            name = split_msg[1]

            # detect user trying to use already allocated name
            if name in self.users:
                print('WARNING: user requested name already registered: ' + name + '\n')
                print('kicking client.\n')

                msg = b'The username you requested: <' + name.encode() + \
                    b'> is already registered. Please reconnect and try again.\n\n' + \
                    b'For assistance, here is the full list of users on server: '
                for user in self.users:
                    print(user)
                    msg += user.encode() + b', '

                from_user.socket.sendall(msg + b'\n')
                time.sleep(0.1) # DEBUG
                from_user.socket.sendall(QUIT_STRING.encode())


                #from_user.socket.close()
                #self.connection_list.remove(from_user.socket)

            # name ok. create new user objects with name
            else:

                from_user.name = name
                #print(name)

                self.connection_dict[name] = from_user # add to dictionary
                #print('added dict key')
                #print(self.connection_dict[name])

                self.users.append(name)
                print("New connection from:", from_user.name)
                from_user.socket.sendall(instructions)


        # detect list rooms request
        elif split_msg[0] == "/rooms": # list rooms
            self.list_rooms(from_user)


        # detect list users request
        elif split_msg[0] == "/list": # list users
            print('I think I got /list')
            if len(split_msg) == 1: # list all users
                #print('got here')
                msg = b'Users on server: '
                #print('---------')
                #print(self.users)
                for user in self.users:
                    print(user)
                    msg += user.encode() + b', '
                    #msg += user + ', '

                #from_user.socket.sendall(msg + b'\n')
            
            else: # list users in specified room
                room_name = split_msg[1]

                if len(self.rooms) == 0:
                    msg = b'No active rooms. Create your own!\n' \
                        + b'Use /join [room_name] to create a room.\n'
                else:
                    if room_name in self.rooms:
                        print(room_name)
                        msg = b'Listing users in [' + room_name.encode() + b']...\n'
                        for test_user in self.connection_dict:
                            if room_name in self.connection_dict[test_user].rooms:
                                msg += test_user.encode() + b', '
                    else:
                        msg = b'The requested room [' + room_name.encode() + b'] does not exist.\n'

            print(msg)

            from_user.socket.sendall(msg + b'\n')


        # detect join room request or switch broadcast room request
        elif split_msg[0] in ["/join", '/switch']: # join room
            #print('I think I got /join or /switch')
            #print(split_msg[0])
            #print(msg)
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
                    #self.rooms.append(new_room)
                    self.rooms[room_name].users.append(from_user)
                    self.rooms[room_name].welcome_new(from_user)
                    from_user.rooms.append(room_name)
                    from_user.current_room = room_name
            
            # user did not provide enough arguments.
            # hit user with hammer of knowledge.
            else:
                from_user.socket.sendall(instructions)


        # detect leave room request
        elif split_msg[0] == "/leave": # leave room
            #print('got to leave')
            if len(split_msg) >= 2: # error check
                room_name = split_msg[1]

                # detect if is request valid (room exists, and user is subscribed
                # to the room)
                if (room_name in self.rooms) and (room_name in from_user.rooms):
                    #print('got to remove user')

                    # remove room from user
                    #del from_user.rooms[room_name]
                    from_user.rooms.remove(room_name)

                    # remove room from Hall
                    self.rooms[room_name].remove_user(from_user)
                    if len(self.rooms[room_name].users) == 0:
                        #print('got to IF')
                        #self.rooms = self.delete_room(room_name) # WTF?
                        self.delete_room(room_name) # WTF?

                    msg = b': You have left ' + room_name.encode() + b'\n'
                        
                # room does not exist
                elif not (room_name in self.rooms):
                    #print('got to does not exist')
                    msg = b'Room [' + room_name.encode() + b'] does not exist.\n'

                # user never joined room
                else:
                    #print('got to never joined')
                    msg = b'You never joined [' + room_name.encode() + b'].\n'

                    from_user.current_room = room_name

                from_user.socket.sendall(msg)


            # user did not provide enough arguments.
            # hit user with hammer of knowledge.
            else:
                msg = b'Usage: /leave [room_name]\n'
                from_user.socket.sendall(msg)


        # detect instructions request
        elif split_msg[0] == "/help": # print instructions
            #print('I think I got /help')
            # user requests hammer of knowledge
            # hit user with hammer of knowledge.
            from_user.socket.sendall(instructions)


        # detect quit request
        elif split_msg[0] == "/quit": # end session
            from_user.socket.sendall(QUIT_STRING.encode())
            self.remove_user(from_user)


        # detect pricate message request
        elif split_msg[0] == "/msg": # private message another user
            #print('I think I got /msg')
            if len(split_msg) >= 3: # error check
                to_user = split_msg[1]
                #print('to_user')
                #print(to_user)
                if to_user in self.connection_dict:
                    send_msg = b'<' + from_user.name.encode() + b'>: ' + \
                    msg.split(' ',2)[2].encode()
                    self.connection_dict[to_user].socket.sendall(send_msg)
                    from_user.socket.sendall(b'\n')
                else: # target user not on server
                    from_user.socket.sendall(b'User <' + to_user.encode() + b'> not found\n')
            else:
                # user did not provide enough arguments.
                # hit user with hammer of knowledge.
                from_user.socket.sendall(instructions)


        # end condition: broadcast, or fail
        else:
            #print('trying to broadcast')
            #print(self.rooms)
            #print(from_user.current_room)
            #print(from_user.name)
            #print(msg)
            if from_user.current_room in self.rooms: # broadcast
                self.rooms[from_user.current_room].broadcast(from_user.name, msg)
            else:
                msg = 'You are currently broadcasting to any room! \n' \
                + 'Use /rooms to see available rooms! \n' \
                + 'Use /join [room_name] to join a room! \n'
                + 'Use /switch [room_name] to switch to a room! \n'

                from_user.socket.sendall(msg.encode())


# ROOM CLASS
# Every room is allocated one.
class Room:
    def __init__(self, name):
        self.users = [] # a list of sockets. This list does not contain names
                        # of users. For names of users connected to rooms, 
                        # refer instead to the list of rooms inside the user class
        self.name = name # the name of the room

    # function to welcome new user
    def welcome_new(self, from_user):
        msg = self.name + " welcomes: " + from_user.name + '\n'
        for user in self.users:
            user.socket.sendall(msg.encode())

    # function to broadcast
    def broadcast(self, from_user_name, msg):
        #print('from_user')
        #print(from_user_name.encode())
        #print(msg)
        msg_out = b'[' + self.name.encode() + b'] ' + from_user_name.encode() + b': ' + msg.encode()

        for user in self.users:
            if user != from_user_name:
                try: 
                    print('user')
                    print(user.name)
                    print(from_user_name)
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
                    print('\nwtf do I do now, Dave?')
                user.socket.sendall(msg_out)


    # # deprecated function. Retained for reference
    # def list(self, from_user):
    #     #print('DEBUG: got to list')
    #     #print(self.users)
    #     if len(self.users) > 0:
    #         print('self.name:')
    #         print(self.name)
    #         msg = b'Users in [' + self.name.encode() + b']: '
    #         for user in self.users:
    #             msg += user.name.encode() + b', '
    #     else:
    #         msg = b'No users in this room.'
    #         # from_user.socket.sendall(msg + b'\n')
    #         return msg


    # function to remove user
    def remove_user(self, from_user):
        self.users.remove(from_user)
        # leave_msg = b'[' + self.name.encode() + b'] ' + \
        #             from_user.name.encode() + b" has left the room\n"
        leave_msg = '<' + self.name + '> ' + \
                    from_user.name + " has left the room\n"
        self.broadcast(from_user.name, leave_msg)


# USER CLASS
# Each user is allocated one.
class User:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket # The socket that select() uses to communicate with
                             # the client process. One client process exists per user
        self.name = name # The name of the user
        self.rooms = [] # List of room names that the user is subscribed to.
        self.current_room = '' # Name of room that user is currently broadcasting to.

    def fileno(self):
        return self.socket.fileno()
