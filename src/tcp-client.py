#!/usr/bin/env python


import logging
import logging.config
import argparse
import sys
import socket

import sys, getopt

from message import FrameData
from construct import *

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
    parser.add_argument("--logconfig", type=str,
                        default="/usr/local/share/tcp-systemd-client-server/logging.conf",
                        help="Path of the log config")
    args = parser.parse_args()

    logging.config.fileConfig(args.logconfig)
    logger = logging.getLogger("Main")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.ip, args.port))

    # Initialize message
    getState = False
    state = False
    dimmer = 255

    if(args.getState == True):
        getState = True
        obj = FrameData.build(Container(GetState = getState, State = state, Dimmer = dimmer))
        s.send(obj)
        data = s.recv(sys.getsizeof(Byte))

        # Use stdout without logger for homebridge script2 compatibility
        if(data == "1"):
            print("Current state = ON")
        else:
            print("Current state = OFF")

    else:
        # Process state
        if(args.state == True):
            logger.info("Send state ON")
            state = True
        else:
            logger.info("Send state OFF")

        # Process dimmer
        if args.dimmer is not None:
            logger.info("Send dimmer")
            dimmer = args.dimmer
        else:
            logger.info("No dimmer")

        obj = FrameData.build(Container(GetState = getState, State = state, Dimmer = dimmer))
        s.send(obj)

    s.close()
