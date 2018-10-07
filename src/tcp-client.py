#!/usr/bin/env python

import sys
import socket

import sys, getopt

TCP_IP = '192.168.22.101'
TCP_PORT = 15333
BUFFER_SIZE = 1024

commands = {
    'on'   : "1",
    'off'  : "2",
    'state': "3"
}

def main(argv):

    command = ''

    try:
        opts, args = getopt.getopt(argv,"hc:",["command="])
    except getopt.GetoptError:
        print 'test.py -c <command>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -c <command>'
            sys.exit()
        elif opt in ("-c", "--command"):
            command = arg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
   
    if command == "on":
        s.send(commands['on'])
    elif command == "off":
        s.send(commands['off'])
    elif command == "state":

        s.send(commands['state'])
        data = s.recv(BUFFER_SIZE)
        s.close()

        if commands['on'] in data:
            print 'true'
        elif commands['off'] in data:
            print 'false'

    else:
        print "wrong parameter : '" + command + "'."
        print type(command)

if __name__ == "__main__":
    main(sys.argv[1:])
