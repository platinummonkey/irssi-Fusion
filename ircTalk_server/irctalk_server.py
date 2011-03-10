#!/usr/bin/env python

### IMPORT
import Queue, time, threading, sys, os, base64, sqlite3, json
from Crypto.Cipher import AES
from socket import *

### Settings (CHANGE THESE and match in irssi settings)
serverHost = '' # localhost
serverPort = 5555 # non-reserved
masterkey = 'mysecretpassword'

### Settings (DON'T CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING)
BLOCK_SIZE = 32 # Block-size for cipher (16, 24 or 32 for AES)
PADDING = '{' # block padding for AES
dataQueue = Queue.Queue()

### ANDROID START
# sufficiently pad text
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

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
	
	def run(self):
		try:
			while True and not self.die: # infinite loop unless called to quit
				connection, address = self.sockobj.accept()
				print 'Server connected by ', address
				# generate cipher and get first IV - prevent same WEP hacks
				self.cipher, self.iv = createCipher(masterkey)
				print "IV:", self.iv.encode('hex')
				connection.send(self.iv) # send iv first
				while True and not self.die: # read from client
					data = connection.recv(10485760)
					if not data: break
					dataCheck, JSON = self.decryptData(data)
					print 'Recieved from Client:', repr(JSON)
					if dataCheck:
						senddata = self.encryptData('SUCCESS')
						print "Size of compresseddata:", len(senddata)
						connection.send(senddata)
						morestuff = 'abc123def456'*int(10000/9)
						senddata = self.encryptData(['test', morestuff, 'test1', {'key': 'value'}, 2223])
						print "Size of compresseddata:", len(senddata)
						connection.send(senddata)
					successReply = connection.recv(256) # only for "END REQUEST"
				connection.close()
		except:
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
		plaintext = self.cipher.decrypt(ciphertext).rstrip(PADDING)
		JSON = json.loads(plaintext)
		return (True, JSON)

	def addToQueue(self, data):
		pass

	def getFromQueue(self):
		pass

### ANDROID END

### DB START
class DBManager(threading.Thread):
	'''DBManager class manages persistent storage for connectivity
  lossses.
  
Table Structure:
PRIMARY_KEY(INT), DATE(TXT), SERVER(TXT), JSON(TXT), SUCCESS(BOOL)
	'''
	def __init__(self, inQueue, outQueue, dbfile=os.getenv("HOME")+"/.irssi/ircTalk.sqlite" ):
		threading.Thread.__init__(self)
		self.inQueue = inQueue
		self.outQueue = outQueue
		self.dbfile = dbfile
		self.connection = sqlite3.connect(self.dbfile)
		self.cursor = self.connection.cursor()
		# here we check to see if the db has been initialized before
		try:
			# if we can't select from the table it will error
			self.cursor.execute('select * from irctalk')
		except:
			# we need to create the table
			self.cursor.execute('create table irctalk (date text, server text, json text, success integer)')
			self.connection.commit()
	
	def run(self):
		pass

### DB END

### IRSSI START
''' The irssi integration is over 2 UNIX sockets and an irssi script

The irssi script connects to both of these one way sockets. The SND
  socket sends raw irssi commands to the irssi script listening socket
  then uses Irssi::command($cmd). These commands must be sanitized and
  are sanitzied in the Android <-> server section before being pushed
  to the database and to irssi. (connection loss between irssi script
  and server makes this a little more robust should anything happen like
  closing irssi :P).
  
irssiSNDSocket:
  accepts new connections over socket-log from the irssi script and a
    new ClientSNDHandler is created (will die after connection is lost)
  recieves JSON elements from events that are interpreted via the
    Android <-> server classes

irssiRCVSocket:
  accepts new connections over socket-remote from the irssi script and a
    new ClientRCVHandler is created (will die after connection is lost)
  sends raw irssi commands to irssi script.
'''
class ircChanNicklist():
	def __init__(self, channel, nicklist=[]):
		self.channel = channel
		self.nicklist = nicklist
	
	def add(self, nicks):
		for n in nicks:
			self.nicklist.append(n)
	
	def remove(self, nicks):
		for n in nicks:
			self.nicklist.remove(n)

class ClientRCVHandler(threading.Thread):
	'''ClientRCVHandler
		manages the connection and queue per connection of the irssi client
	'''
	def __init__(self, connection, queue):
		self.connection = connection
		self.queue = queue
		threading.Thread.__init__(self)
		
	def run(self):
		try:
			while True:
				data = self.connection.recv(10485760)
				if data:
					JSON = json.loads(data)
					self.addToQueue(JSON)
		except:
			print "Client RECV Handler Exception"
			self.connection.close()

	def addToQueue(self, data):
		'''blocking queue add'''
		try:
			return self.queue.put(data)
		except:
			return None

class ClientSNDHandler(threading.Thread):
	'''ClientSNDHandler
		manages the connection and queue per connection of the irssi client
	'''
	def __init__(self, connection, queue):
		self.connection = connection
		self.queue = queue
		threading.Thread.__init__(self)
		
	def run(self):
		try:
			while True:
				JSON = self.getFromQueue() # '{"cmd": "msg #channel some message"}'
				if JSON:
					print "data:", repr(JSON)
					irssiCMD = json.loads(JSON) # {"cmd": "msg #channel some message"}
					self.connection.send(irssiCMD["cmd"])
		except:
			print "Client SEND Handler Exception"
			self.connection.close()
	
	def getFromQueue(self):
		try:
			# try to get next thing from queue - NONBLOCKING
			return self.queue.get_nowait()
		except:
			# Queue was empty, so don't return anything
			return None

class irssiRCVSocket(threading.Thread):
	'''irssiRCVSocket(unixsocket)
	
	This is the recieving irssi socket that always listens for irssi 
		logs using the irssiTalk script for irssi.
	
	Options:
		queue is the dataqueue shared between SND and RCV
			default is None and will raise and ERROR!
		unixsocket is the path to the fifo to be used
			default is $ENV{'HOME'}/.irssi/socket-log
			
			does not have to be pre-existing! but your irssi variable
			must also match!
	'''
	def __init__(self, queue=None,  unixsocket = os.getenv("HOME")+"/.irssi/socket-log"):
		if os.access(unixsocket, 0):
			os.remove(unixsocket)
		self.queue = queue
		try:
			self.socket_file = unixsocket
			self.sockobj = socket(AF_UNIX, SOCK_STREAM) # create TCP socket obj
			self.sockobj.bind(unixsocket) # bind socket to port
			self.sockobj.listen(1)  # listen, allow 1 connection only
		except:
			print "Error starting server"
			sys.exit(0)
		threading.Thread.__init__(self)
		self.die = False # loop killer
	
	def run(self):
		try:
			while True and not self.die: # infinite loop unless called to quit
				self.connection, self.address = self.sockobj.accept()
				clienthandle = ClientRCVHandler(self.connection, self.queue)
				clienthandle.start()
		except:
			print "Exception in Main RECV Server"
	
	def kill(self):
		self.die = True
		self.connection.close()
		self.sockobj.close()

class irssiSNDSocket(threading.Thread):
	'''irssiSNDSocket(unixsocket)
	
	This is the sending irssi socket that always sends commands to irssi 
		using the irssiTalk script for irssi.
	
	Options:
		queue = the internal queue to send to irssi
		
		unixsocket is the path to the fifo to be used
			default is $ENV{'HOME'}/.irssi/socket-remote
			
			does not have to be pre-existing! but your irssi variable
			must also match!
	'''
	def __init__(self, queue = None, unixsocket = os.getenv("HOME")+"/.irssi/socket-remote"):
		self.queue = queue
		if os.access(unixsocket, 0):
			os.remove(unixsocket)
		
		try:
			self.socket_file = unixsocket
			self.sockobj = socket(AF_UNIX, SOCK_STREAM) # create TCP socket obj
			self.sockobj.bind(unixsocket) # bind socket to port
			self.sockobj.listen(1)					   # listen, allow 1 connection only
		except:
			print "Error starting irssi SEND server"
			sys.exit(0)
		threading.Thread.__init__(self)
		self.die = False # loop killer
	
	def run(self):
		try:
			while True and not self.die: # infinite loop unless called to quit
				self.connection, self.address = self.sockobj.accept()
				clienthandle = ClientSNDHandler(self.connection, self.queue)
				clienthandle.start()
		except:
			# server failed to start - maybe sockets already binded?
			self.kill()
	
	def kill(self):
		try:
			self.die = True
			self.connection.close()
			self.sockobj.close()
		except:
			pass

### IRSSI END


### MAIN
''' Server/Thread Class creation starts here

This is where the irssiSNDSocket, irssiRCVSocket, IRCTalkServer ... 
  threads are
  initialized and then started. The server will not end until all
  threads have rejoined. must be killed otherwise.

TODO:
  - daemon mode
  - allow server command input from shell (ie. start irssiServers)
'''
#serverThread = IRCTalkServer(masterkey, serverHost, serverPort)
#serverThread.start()
#serverThread.join()
a = irssiSNDSocket(queue=dataQueue)
b = irssiRCVSocket(queue=dataQueue)
a.start()
b.start()
numb=1
while True:
	if dataQueue.empty():
		dataQueue.put({"reply":numb})
		numb=numb+1
		print "number:", numb

a.join()
#b.join()

print 'Main thread exiting'
