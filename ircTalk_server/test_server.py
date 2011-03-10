#!/usr/bin/env python

import os, time, threading, json
from socket import *

class ClientHandler(threading.Thread):
    def __init__(self, connection):
        self.connection = connection
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            while True:
                data = self.connection.recv(10485760)
                if not data: break
                #JSON = json.loads(data)
                #print "data:", repr(JSON)
                print "data:", repr(data)
        except:
            print "Client Handler Exception"
            self.connection.close()

class Server(threading.Thread):
    def __init__(self, address):
        self.serversock = socket(AF_UNIX, SOCK_STREAM)
        self.serversock.bind(address)
        self.serversock.listen(1)
        threading.Thread.__init__(self)
    
    def run(self):
        self.iServer = 1
        while True:
            clientsock, clientaddr = self.serversock.accept()
            print "Server connected by peer at", time.time()
            clienthandle = ClientHandler(clientsock)
            clienthandle.start()
            print "server number:", repr(self.iServer)
            self.iServer = self.iServer +1

class SNDClientHandler(threading.Thread):
    def __init__(self, connection):
        self.connection = connection
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            while True:
                time.sleep(5)
                self.connection.send("msg pltmnky test")
        except:
            print "Client Handler Exception"
            self.connection.close()

class SNDServer(threading.Thread):
    def __init__(self, address):
        self.serversock = socket(AF_UNIX, SOCK_STREAM)
        self.serversock.bind(address)
        self.serversock.listen(1)
        threading.Thread.__init__(self)
    
    def run(self):
        self.iServer = 1
        while True:
            clientsock, clientaddr = self.serversock.accept()
            print "Server connected by receiving peer at", time.time()
            clienthandle = SNDClientHandler(clientsock)
            clienthandle.start()
            print "sending server number:", repr(self.iServer)
            self.iServer = self.iServer +1


fifosocket = '/home/platinummonkey/.irssi/socket-log'
SNDfifosocket = '/home/platinummonkey/.irssi/socket-remote'

if os.access(fifosocket, 0):
	os.remove(fifosocket)

if os.access(SNDfifosocket, 0):
	os.remove(SNDfifosocket)

testserver = Server(fifosocket)
testserverSND = SNDServer(SNDfifosocket)
testserver.start()
testserverSND.start()
testserver.join()
testserverSND.join()
