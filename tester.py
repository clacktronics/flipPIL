import sys, numpy, os, serial 
from PIL import Image, ImageDraw 
from time import sleep 

dots = serial.Serial('/dev/ttyAMA0',57600) 


message = ([0x00]*32) 
message[0] = 0x80 # Header 
message[1] = 0x83 # Mode 
message[2] = 0x01 # Panel Addresss
message[-1] = 0x8F
 
refresh = bytearray([0x80,0x82,0x8F]) 

adds = [11,4,14,19,9,16,15,10,43,36,46,51,41,48,47,42]
x = 0
while True:
	for m in range(5):
	        for i in range(28):
        	    message[i+3] = 0x7F
        	values = bytearray(message)
        	dots.write(values)
        	dots.write(refresh)
	        sleep(.1)

       		for i in range(28):
            		message[i+3] = 0x00
        	values = bytearray(message)
        	dots.write(values)
        	dots.write(refresh)
	        sleep(.1)

	x += 1
	if x > 63: x = 0
        message[2] = x #adds[x]
