#!/usr/bin/env python

import logging
import logging.config
import argparse
import socket
import threading
import dbus

from message import FrameData

class ServiceManager(object):
    def __init__(self, unitName):
        self.logger = logging.getLogger("ServiceManager")

        if ".service" not in unitName:
            self.logger.debug("Add .service extension to the unit name.")
            self.unitName = unitName + ".service"
        else:
            print "IN"
            self.unitName = unitName
            
        self.sysbus = dbus.SystemBus()
        self.systemd1 = self.sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.manager = dbus.Interface(self.systemd1, 'org.freedesktop.systemd1.Manager')
        self.unit = self.manager.LoadUnit(self.unitName)
        self.proxy = self.sysbus.get_object('org.freedesktop.systemd1', str(self.unit))

    def start(self):
        self.manager.StartUnit(self.unitName, "fail")
        self.logger.debug(self.unitName + " started")

    def stop(self):
        self.manager.StopUnit(self.unitName, "fail")
        self.logger.debug(self.unitName + " stopped")

    def getState(self):
        result = False
        activeState = self.proxy.Get('org.freedesktop.systemd1.Unit',
                         'ActiveState',
                         dbus_interface='org.freedesktop.DBus.Properties')
        self.logger.debug("State = " + activeState)
        
        if(activeState == 'active'):
            result = True
            
        return result
        

class ThreadedServer(object):
    def __init__(self, host, port, serviceManager):
        self.logger = logging.getLogger("ThreadedServer")
        self.host = host
        self.port = port
        self.serviceManager = serviceManager
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:

            data = client.recv(FrameData.sizeof())

            if data:
                obj = FrameData.parse(data[:FrameData.sizeof()])
                state = False
                self.logger.debug(obj)

                if(obj.State == True):
                    self.logger.info("State ON")
                    self.serviceManager.start()
                else:
                    self.logger.info("State OFF")
                    self.serviceManager.stop()

                if(obj.GetState == True):
                    self.logger.info("Get State")
                    state = self.serviceManager.getState()

                if(obj.Dimmer != 0xFF):
                    self.logger.info("Dimmer OK")
                else:
                    self.logger.info("No Dimmer")

                # Set the response to echo back the recieved data 
                response = str(int(state == True))
                client.send(response)
            else:
                raise error('Client disconnected')

            client.close()
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int,
                        help="Port to listen")
    parser.add_argument("unitName", type=str,
                        help="Systemd service name")
    args = parser.parse_args()

    logging.config.fileConfig("logging.conf")

    serviceManager = ServiceManager(args.unitName)
    ThreadedServer('',args.port, serviceManager).listen()
