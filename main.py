
'''
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
-------------------------------------------------------
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
-------------------------------------------------------
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
-------------------------------------------------------
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
-------------------------------------------------------
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
-------------------------------------------------------
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
x x x x x x x x x x x x x x x x x x x x x x x x x x x x
'''

import sys, numpy, os, serial
from PIL import Image, ImageDraw
from time import sleep

dots = serial.Serial('/dev/tty.usbserial-A50285BI',115200)

# 28 + 3 headers and 1 end
# upper list = row order
# sub-list = columb order
# e.g 2 x 2 segments = [[1,2],[3,4]]

Segment_arr = [[1],[2],[3],[12],[5],[6]]

seg_out = []
for row_n, seg_row in enumerate(Segment_arr):
    for col_n,seg_col in enumerate(seg_row):
        seg_out.append([0x00]*32)
        seg_out[row_n][0] = 0x80 # Header
        seg_out[row_n][1] = 0x83 # Mode
        seg_out[row_n][2] = Segment_arr[row_n][col_n] # Panel Addresss

img = Image.new('L',(42,28),255)
drw = ImageDraw.Draw(img)
drw.ellipse((0,0,8,8), fill=0)

# the raw x y grid to wirte to
grd = [['X' for x in range(42)] for y in range(28)]

# for x in grd:
#     for y in x:
#         print y,
#     print ''

def toGraphic(inp):
    outp = [['X' for x in range(42)] for y in range(28)]
    for xn, x in enumerate(inp):
        for yn, y in enumerate(x):
            if y == 255:
                outp[xn][yn] = '.'
            else:
                outp[xn][yn] = '0'
    return outp

def toBytes(inp):
    output = seg_out[:]
    out = 0
    for xn, x in enumerate(inp):
        seg = 0
        for yn,y in enumerate(x):
            b = 2 ** (yn % 7)
            if y == '0':
                out += b
            if yn % 7 == 0:
                #print "(%d : %d) %s" % (xn,yn,bin(out))
                output[yn/7][xn+3] = out
                out = 0
    return output

ix = 0
iy = 0
inx = 1
iny = 1
bsize = 18

refresh = [0x80,0x82,0x8F]

while True:

    ix += inx
    iy += iny

    if (ix+bsize) > 42 or ix < 0: inx *=-1
    if (iy+bsize) > 28 or iy < 0: iny *=-1


    img = Image.new('L',(42,28),255)
    drw = ImageDraw.Draw(img)
    drw.ellipse((ix,iy,ix+bsize,iy+bsize), fill=0)
    ll =  numpy.array(img)
    graphic = toGraphic(ll)
    data = toBytes(graphic)

    for message in data:
        values = bytearray(message)
        print message
        dots.write(values)
        dots.write(refresh)

    for row in graphic:
        for y in row:
            print y,
        print ''
    print '\n'

    sleep(.1)



# out = 0
# for xn, x in enumerate(grd):
#     seg = 0
#     for yn,y in enumerate(x):
#         b = 2 ** (yn % 7)
#         if y == '0':
#             out += b
#         if yn % 7 == 0:
#             #print "(%d : %d) %s" % (xn,yn,bin(out))
#             seg_out[yn/7][xn+3] = out
#             out = 0

# for row in seg_out:
#     print row







# import serial
# from time import sleep
#
# dots = serial.Serial('/dev/tty.usbserial-A50285BI',9600)
#
# frame_segment = [0x00]*32
# refresh = [0x80,0x82,0x8F]
#
# frame_segment[0] = 0x80 # Header
# frame_segment[1] = 0x83 # Mode
# frame_segment[2] = 0x00 # Panel Addresss
#
# frame_segment[31] = 0x8F # End
#
#
#
# out = 0
# for n,i in enumerate(['X','X','X','0']):
#     b = 2 ** n
#     if i == '0':
#         out += b
#         print bin(out)





# while True:
#
#     for i in range(3,31):
#         frame_segment[i] = 0x7F
#
#     print "Sending On"
#     dots.write(frame_segment)
#     dots.write(refresh)
#     sleep(1)
#
#     for i in range(3,31):
#         frame_segment[i] = 0x0
#
#     print "Sending Off"
#     dots.write(frame_segment)
#     dots.write(refresh)
#     sleep(1)
