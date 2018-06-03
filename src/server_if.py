import argparse
import socket
import time
import yaml

#from IRC_server import IRC_server_12DOF

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
            default='config_12DOF.yaml',
            help='IRC_server configuration file')

    return parser.parse_args()

def initialize_IRC_server(config_file):
    # open config file
    with open(config_file) as f:
        my_config = yaml.load(f)

    my_IRC_server = IRC_server_12DOF(my_config)
    my_IRC_server.move_all_legs(raise_value=0, rotate_value=100)
    time.sleep(1)
    my_IRC_server.move_all_legs(raise_value=100, rotate_value=100)
    time.sleep(1)
    my_IRC_server.move_all_legs(raise_value=0, rotate_value=100)

    return my_IRC_server


def command_processor(data, my_IRC_server):
    print('Data: {}'.format(data))

    arguments = data.split()
    if len(arguments) == 1:
        command = arguments[0]
        iteration = 1

    elif len(arguments) == 2:
        command = arguments[0]
        iteration = int(arguments[1])

    else:
        return 'ERROR: invalid command format'

    print('Command: {}'.format(command))
    print('Iteration: {}'.format(iteration))

    commands = [
        'go_forward' #new
        'go_back' #new
        'turn_left' #modify
        'turn_right' #modify
        'walk_forward', #remove
        'walk_backward', #remove
        'front_dancing_1', #remove
        'front_dancing_2', #remove
        'back_dancing_1', #remove
        'back_dancing_2', #remove
    ]

    if command == 'turn_left':
        for i in range(iteration):
            print('turning left...')
            my_IRC_server.turn_left()

        return ('Turning Left {} times'.format(iteration))

    elif command == 'turn_right':
        for i in range(iteration):
            print('turning right...')
            my_IRC_server.turn_right()

        return ('Turning Right {} times'.format(iteration))

    elif command == 'walk_forward':
        for i in range(iteration):
            print('walking forward...')
            if i%2:
                my_IRC_server.left_right_left_step()
            else:
                my_IRC_server.right_left_right_step()

        return ('Walking Forward {} times'.format(iteration))

    elif command == 'walk_backward':
        for i in range(iteration):
            print('walking backward...')
            if i%2:
                my_IRC_server.left_right_left_step_back()
            else:
                my_IRC_server.right_left_right_step_back()

        return ('Walking Backward {} times'.format(iteration))

    elif command == 'front_dancing_1':
        print('getting ready to dance...')
        my_IRC_server.reposition_center_legs(0)
        my_IRC_server.move_center_legs(raise_value=100)

        print('ready to dance...')
        for i in range(iteration):
            print('front dancing...')
            my_IRC_server.front_leg_dancing(step=1)

        print('cleaning up from dancing...')
        my_IRC_server.reposition_center_legs(100)

        return ('Dancing Front Legs {} times'.format(iteration))

    elif command == 'front_dancing_2':
        print('getting ready to dance...')
        my_IRC_server.reposition_center_legs(0)
        my_IRC_server.move_center_legs(raise_value=100)

        print('ready to dance...')
        for i in range(iteration):
            print('front dancing...')
            my_IRC_server.front_leg_dancing(step=2)

        print('cleaning up from dancing...')
        my_IRC_server.reposition_center_legs(100)

        return ('Dancing Front Legs {} times'.format(iteration))

    elif command == 'back_dancing_1':
        print('getting ready to dance...')
        my_IRC_server.reposition_center_legs(100)
        my_IRC_server.move_center_legs(raise_value=100)

        print('ready to dance...')
        for i in range(iteration):
            print('front dancing...')
            my_IRC_server.back_leg_dancing(step=1)

        print('cleaning up from dancing...')
        my_IRC_server.reposition_center_legs(100)

        return ('Dancing Back Legs {} times'.format(iteration))

    elif command == 'back_dancing_2':
        print('getting ready to dance...')
        my_IRC_server.reposition_center_legs(100)
        my_IRC_server.move_center_legs(raise_value=100)

        print('ready to dance...')
        for i in range(iteration):
            print('front dancing...')
            my_IRC_server.back_leg_dancing(step=2)

        print('cleaning up from dancing...')
        my_IRC_server.reposition_center_legs(100)

        return ('Dancing Back Legs {} times'.format(iteration))

    elif command == 'commands':
        temp = 'Implemented Commands: '
        for command in commands:
            temp += command + ', '

        return temp

    else:
        print('ERROR: command not recognized: {}'.format(command))
        return 'Command not found!'

def listenToClient(client, address, my_IRC_server):
    size=1024
    while True:
        try:
            data = client.recv(size).decode()
            if data:
                # Read command from client
                print("from connected user: " + str(data))
                response = command_processor(data, my_IRC_server)

                # data = str(data).upper()
                client.send(response.encode())
            else:
                raise error('Client disconnected')
        except:
            client.close()
            return False

def Main(host, port, config_file):
    my_IRC_server = initialize_IRC_server(config_file)

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(5)
    while True:
        client, address = mySocket.accept()
        client.settimeout(300)
        print ("Connection from: " + str(address))
        listenToClient(client, address, my_IRC_server)

if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))
    print('Config File: {}'.format(args.config_file))

    Main(args.host, args.port, args.config_file)
