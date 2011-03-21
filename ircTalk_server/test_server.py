#!/usr/bin/env python

import os, time, threading
import simplejson as json
from socket import *
import sys, base64, Queue

from Crypto.Cipher import AES
from socket import *

### Settings (CHANGE THESE and match in irssi settings)
serverHost = '' # localhost
serverPort = 5555 # non-reserved
masterkey = 'mysecretpassword'

### Settings (DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING)
BLOCK_SIZE = 16 # Block-size for cipher (16, 24 or 32 for AES)
KEY_MULT_SIZE = 16 # key size must be a multiple of this
#PADDING = '{' # block padding for AES
dataQueue = Queue.Queue()

### ANDROID START
# sufficiently pad text
#pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
# PKCS5 Padding
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
keypad = lambda s: s + (KEY_MULT_SIZE - len(s) % KEY_MULT_SIZE) * chr(KEY_MULT_SIZE - len(s) % KEY_MULT_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

#print "pad(masterkey)", repr(pad(masterkey))
#print "keypad(masterkey)", repr(keypad(masterkey))

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
				#paddedKey = keypad(masterkey)
				#print "master key:", masterkey, " - padded key:", paddedKey, " - diff key:", keypad('test')
				#self.ecipher, self.iv = createCipher(masterkey)
				#self.dcipher, self.iv = createCipher(masterkey)
				#print "IV:", self.iv.encode('hex'), "Sending IV: ", repr(self.iv)
				#connection.send("%s%s" % (self.iv.encode('hex'),'\n')) # send iv first
				while True and not self.die: # read from client
					print "waiting for client"
					data = connection.recv(10485760)
					print "recieved from client:", repr(data.rstrip())
					if not data:
                                                print "NO DATA"
                                                break
					#dataCheck, JSON = self.decryptData(data.rstrip())
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
					#senddata = self.encryptData(r'test')
					#senddata = "%s%s" % ('test', '\n');
					plaintext = {'server': 'irc.freenode.org',
								'channel': '#somechannel',
								'messages': [
									{'time': '12:44', 'nick': 'dude', 'address': 'dude@someplace.com', 'message': 'man that was a crazy day'},
									{'time': '12:45', 'nick': 'noob', 'address': 'noob@149.133.14.11', 'message': 'yeah it was, i can\'t believe that we found that place!'},
									{'time': '12:46', 'nick': 'noob0', 'address': 'noob@149.133.14.0', 'message': 'yup 0'},
									{'time': '12:47', 'nick': 'noob1', 'address': 'noob@149.133.14.1', 'message': 'yup 1'},
									{'time': '12:47', 'nick': 'noob2', 'address': 'noob@149.133.14.2', 'message': 'yup 2'},
									{'time': '12:48', 'nick': 'noob3', 'address': 'noob@149.133.14.3', 'message': 'yup 3'},
									{'time': '12:49', 'nick': 'noob4', 'address': 'noob@149.133.14.4', 'message': 'yup 4'},
									{'time': '12:49', 'nick': 'noob5', 'address': 'noob@149.133.14.5', 'message': 'yup 5'},
									{'time': '12:49', 'nick': 'noob6', 'address': 'noob@149.133.14.6', 'message': 'yup 6'},
									{'time': '12:50', 'nick': 'noob7', 'address': 'noob@149.133.14.7', 'message': 'yup 7'},
									{'time': '12:50', 'nick': 'noob8', 'address': 'noob@149.133.14.8', 'message': 'yup 8'},
									{'time': '12:51', 'nick': 'noob9', 'address': 'noob@149.133.14.9', 'message': 'yup 9'},
									]
								}
					print "set up plaintext:", repr(plaintext)
					JSON = json.dumps(plaintext, separators=(',',':'))
					print "json dump:", repr(JSON)
					print "reply data:", repr(JSON)
					connection.send("%s\n" % JSON)
					#connection.send("Hello back mr android!")
					#successReply = connection.recv(256) # only for "END REQUEST"
                                        break
                                print "Closing connection... \n\n"
				connection.close()
		except:
                        print "exception on try loop"
			pass # an error occurred, just drop it, the client will try again later
	
	def encryptData(self, plaintext):
		# convert to json string, pad the string, then encrypt, then compress
		#JSON = json.dumps(plaintext, separators=(',',':'))
		JSON = plaintext
		#print "Size of JSON:", len(JSON)
		ciphertext = pad(JSON.encode('utf8'))
		print "padded text:", repr(ciphertext)
		ciphertext = self.ecipher.encrypt(ciphertext)
		print "ciphertext:", repr(ciphertext), "|", len(ciphertext), "|", ciphertext
		#ciphertext = ciphertext.encode('hex').upper()
		#print "hexified text:", repr(ciphertext)
		#ciphertext = self.cipher.encrypt(pad(JSON)).encode('hex').upper()
		print "Size of ciphertext:", len(ciphertext)
		return ciphertext
	
	def decryptData(self, ciphertext):
		try:
			# decompress data to ciphertext, decrypt, convert to json
			print "length of ciphertext:", len(ciphertext)
			ptext = ciphertext.decode('hex')
			print "unhexifed:", repr(ptext)
			ptext = self.dcipher.decrypt(ptext)
			print "decrypted:", repr(ptext)
			ptext = unpad(ptext)
			print "unpadded:", repr(ptext)
			#ptext = unpad(self.cipher.decrypt(ciphertext.decode('hex')))
			print "ptext: ", repr(ptext)
			JSON = ptext
			#plaintext = unpad(self.cipher.decrypt(ciphertext))
			##JSON = json.loads(plaintext)
			#JSON = plaintext
		except:
			print "Error on decryption"
			JSON = None
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
