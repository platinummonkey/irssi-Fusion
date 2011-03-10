#!/usr/bin/env python

import sys, os, zlib, json
from Crypto.Cipher import AES
from socket import *
serverHost = 'localhost'
serverPort = 5555

masterkey = 'mysecretpassword'

BLOCK_SIZE = 32 # Block-size for cipher (16, 24 or 32 for AES)
PADDING = '{' # block padding for AES

# sufficiently pad text
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# generate new IV's - why you ask? ... just look at WEP
def createCipher(key, iv):
	return AES.new(key, AES.MODE_CBC, iv)


message = ['hello']

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

# get IV
iv = sockobj.recv(16)
print 'IV:', iv.encode('hex')
cipher = createCipher(masterkey, iv)

def encodeText(cipher, text):
	JSON = json.dumps(text)
	ciphertext = cipher.encrypt(pad(JSON))
	return zlib.compress(ciphertext)

def decodeText(cipher, data):
	ciphertext = zlib.decompress(data)
	plaintext = cipher.decrypt(ciphertext).rstrip(PADDING)
	JSON = json.loads(plaintext)
	return JSON


sockobj.send(encodeText(cipher, message))
data = sockobj.recv(10485760)
newdata = decodeText(cipher, data)
print 'Client received:', repr(newdata)
data = sockobj.recv(10485760)
newdata = decodeText(cipher, data)
print 'Client received:', repr(newdata)
sockobj.send(encodeText(cipher, "END REQUEST"))

sockobj.close()
