# -*- coding: utf-8 -*-

# svr.py

# server for remote versions of the w and ps commands

# user can check load on machine without logging in (or even without
# having an account on the remote machine)

# usage:

# python svr.py port_num

import socket,sys,os
 
def main():

  # create listening socket
  ls = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
  port = int(sys.argv[1])
  ls.bind(('', port))
  
  # enter listening loop
  while (1):
    # accept "call" from client
    ls.listen(1)
    (conn, addr) = ls.accept()
    print('client is at', addr)
    # get and run command from client, then get its output
    rc = conn.recv(2)
    # run the command in a Unix-style pipe
    ppn = os.popen(rc)
    # ppn is a "file-like object," so can apply readlines()
    rl = ppn.readlines()
    # create a file-like object from the connection socket
    flo = conn.makefile('w',0) # write-only, unbuffered
    flo.writelines(rl[:-1])
    # clean up
    # must close both the socket and the wrapper
    flo.close()
    conn.close()

if __name__ == '__main__':
  main()