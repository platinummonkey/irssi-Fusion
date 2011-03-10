#!/usr/bin/env python

import os, time, threading, json
from socket import *
import sys, base64, Queue

from Crypto.Cipher import AES
from socket import *

### Settings (CHANGE THESE and match in irssi settings)
serverHost = '' # localhost
serverPort = 5555 # non-reserved
masterkey = 'mysecretpassword'

### Settings (DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING)
BLOCK_SIZE = 32 # Block-size for cipher (16, 24 or 32 for AES)
#PADDING = '{' # block padding for AES
dataQueue = Queue.Queue()

### ANDROID START
# sufficiently pad text
#pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
# PKCS5 Padding
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCKSIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

# generate new IV's - why you ask? ... just look at WEP
def createCipher(key):
	iv = os.urandom(16)
	return (AES.new(key, AES.MODE_CBC, iv), iv)

class IRCTalkServer(threading.Thread):
	def __init__(self, masterkey, host='', port=5555):
		try:
			self.sockobj = socket(AF_INET, SOCK_STREAM) # create TCP socket obj
			self.sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # make port reusable
			self.sockobj.bind((host, port)) # bind socket to port
			self.sockobj.listen(5)					   # listen, allow 5 pending connects
			if host == '': host='localhost'
			print "Started server on %s:%d" % (host, port)
		except:
			print "Error starting server"
			sys.exit(0)
		threading.Thread.__init__(self)
		self.die = False # loop killer
		self.masterkey = masterkey
		self.host = host
		self.port = port
	
	def run(self):
		try:
			while True and not self.die: # infinite loop unless called to quit
				connection, address = self.sockobj.accept()
				print 'Server connected by ', address
				# generate cipher and get first IV - prevent same WEP hacks
				#self.cipher, self.iv = createCipher(masterkey)
				#print "IV:", self.iv.encode('hex')
				#connection.send(self.iv) # send iv first
				while True and not self.die: # read from client
					data = connection.recv(10485760)
					if not data:
                                                print "NO DATA"
                                                break
					#dataCheck, JSON = self.decryptData(data)
					#print 'Recieved from Client:', repr(JSON)
					print 'Recieved from Client:', repr(data)
					#if dataCheck:
						#senddata = self.encryptData('SUCCESS')
						#print "Size of compresseddata:", len(senddata)
						#connection.send(senddata)
						#morestuff = 'abc123def456'*int(10000/9)
						#senddata = self.encryptData(['test', morestuff, 'test1', {'key': 'value'}, 2223])
						#print "Size of compresseddata:", len(senddata)
						#connection.send(senddata)
					print "Sending reply to client..."
					connection.send("Hello back mr android!")
					#successReply = connection.recv(256) # only for "END REQUEST"
                                        break
                                print "Closing connection..."
				connection.close()
		except:
                        print "exception on try loop"
			pass # an error occurred, just drop it, the client will try again later
	
	def encryptData(self, text):
		# convert to json string, pad the string, then encrypt, then compress
		JSON = json.dumps(text, separators=(',',':'))
		print "Size of JSON:", len(JSON)
		ciphertext = self.cipher.encrypt(pad(JSON))
		print "Size of ciphertext:", len(ciphertext)
		return ciphertext
	
	def decryptData(self, data):
		# decompress data to ciphertext, decrypt, convert to json
		ciphertext = data
		plaintext = unpad(self.cipher.decrypt(ciphertext))
		JSON = json.loads(plaintext)
		return (True, JSON)

	def addToQueue(self, data):
		pass

	def getFromQueue(self):
		pass

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


#fifosocket = '/home/platinummonkey/.irssi/socket-log'
#SNDfifosocket = '/home/platinummonkey/.irssi/socket-remote'

#if os.access(fifosocket, 0):
	#os.remove(fifosocket)

#if os.access(SNDfifosocket, 0):
	#os.remove(SNDfifosocket)

#testserver = Server(fifosocket)
#testserverSND = SNDServer(SNDfifosocket)
#testserver.start()
#testserverSND.start()
#testserver.join()
#testserverSND.join()

testserver =IRCTalkServer(masterkey)
testserver.start()
testserver.join()
