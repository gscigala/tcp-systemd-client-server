#!/usr/bin/env python


import logging
import logging.config
import argparse
import sys
import socket

import sys, getopt

from message import FrameData

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str,
                        help="Destination address")
    parser.add_argument("port", type=int,
                        help="Port to listen")
    parser.add_argument("--getState", type=int,
                        help="Get state of the device")
    parser.add_argument("--state", type=int,
                        help="Set state of the device")
    parser.add_argument("--dimmer", type=int,
                        help="Set dimmer of the device")
    args = parser.parse_args()

    logging.config.fileConfig("logging.conf")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.ip, args.port))

    # Initialize message
    obj = FrameData.parse(data[:FrameData.sizeof()])
    obj.GetState = False
    obj.State = False
    obj.Dimmer = 255

    if(args.getState == True):
        self.logger.info("Get State")
        obj.GetState = True
        s.send(obj)
        data = s.recv(BUFFER_SIZE)

        #TODO process received frame

    else:
        # Process state
        if(args.state == True): #TODO test if exist too !
            self.logger.info("Send state ON")
            obj.State = True
        else:
            self.logger.info("Send state OFF")

        # Process dimmer
        if (args.dimmer != 255):
            self.logger.info("Send dimmer")
            obj.Dimmer = args.dimmer
        else:
            self.logger.info("No dimmer")

        s.send(obj)
        
        

"""
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
"""
