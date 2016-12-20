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

while True:
        for i in range(28):
            message[i+3] = 0x7F
        values = bytearray(message)
        dots.write(values)
        dots.write(refresh)
	print message
        sleep(1)
        for i in range(28):
            message[i+3] = 0x00
        values = bytearray(message)
        dots.write(values)
        dots.write(refresh)
        print message
        sleep(1)
