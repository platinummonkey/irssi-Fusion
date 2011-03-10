#!/usr/bin/env python

import sys, os, zlib, json, Queue, time
#from Crypto.Cipher import AES
from socket import *
#serverHost = 'localhost'
#serverPort = 5555
unixRCVsocket = '/home/platinummonkey/.irssi/socket-remote'
#unixRCVsocket = '/home/platinummonkey/fifo_socket_test_server'
unixSNDsocket = '/home/platinummonkey/.irssi/socket-log'

message = {'sending':['hello', 'there']}

messageQueue = Queue.Queue()

#sockobjSND = socket(AF_UNIX, SOCK_STREAM)
#sockobjSND.connect(unixSNDsocket)
sockobjRCV = socket(AF_UNIX, SOCK_STREAM)
sockobjRCV.connect(unixRCVsocket)
sockobjRCV.setblocking(False)

def encodeText(text):
	JSON = json.dumps(text)
	return JSON

def decodeText(data):
	print repr(data)
	JSON = json.loads(data)
	return JSON


#sockobjSND.send(encodeText(message))
#i = 0
#while i <= 100:
	#time.sleep(0.005)
	#try:
		#data = sockobjRCV.recv(10485760)
		##print "Client Raw Recieve:", repr(data)
		#messageQueue.put("Client Raw Recieve: %s" % repr(data))
		#newdata = decodeText(data)
		##print 'Client received:', repr(newdata)
		#messageQueue.put("Client recieved: %s" % repr(newdata))
		#i = i + 1
	#except:
		##print "No DATA AVAILABLE FROM SERVER"
		#messageQueue.put("NO DATA AVAILABLE FROM SERVER")

#while not messageQueue.empty():
	#try:
		#print messageQueue.get_nowait(), "\n"
	#except:
		#pass

data = sockobjRCV.recv(10485760)
newdata = decodeText(cipher, data)
print 'Client received:', repr(newdata)
sockobj.send(encodeText(cipher, "END REQUEST"))

sockobjSND.close()
sockobjRCV.close()
