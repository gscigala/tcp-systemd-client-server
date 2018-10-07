#!/usr/bin/env python

import socket
import dbus

TCP_IP = '192.168.22.101'
TCP_PORT = 15333
BUFFER_SIZE = 1024

commands = {
    'on'   : "1",
    'off'  : "2",
    'state': "3"
    }

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
unit = manager.LoadUnit('connected-clock.service')
proxy = sysbus.get_object('org.freedesktop.systemd1', str(unit))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print "received data:", data
        
        if commands['on'] in data:
            manager.StartUnit('connected-clock.service', "fail")
            print "Connected Clock started"
            
        elif commands['off'] in data:
            manager.StopUnit('connected-clock.service', "fail")
            print "Connected Clock stopped"
            
        elif commands['state'] in data:
            print "Send Connceted Clock state"

            result = commands['off']

            activeState = proxy.Get('org.freedesktop.systemd1.Unit',
                'ActiveState',
                dbus_interface='org.freedesktop.DBus.Properties')

            if(activeState == 'active'):
                result = commands['on']

            conn.send(result)  # echo
            
    conn.close()
    print "Connection closed"
