from PIL import Image
import numpy
from flipil import flipil
import socket

foreground = 255
background = 0
direction = "down"

panel_arr = [
	    [31,63],[30,62],[29,61],[28,60],[27,59],[26,58],[25,57],[24,56],
	    [23,55],[22,54],[21,53],[20,52],[19,51],[18,50],[17,49],[16,48],
	    [15,47],[14,46],[13,45],[12,44],[11,43],[10,42],[9,41],[8,40],
	    [7,39],[6,38],[5,37],[4,36],[3,35],[2,34],[1,33],[0,32]
	    ]


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]



    def init_panel():
        panel1 = flipil("alfa_zeta", [28,7], panel_arr, init_color = 0)
        panel1.set_port('/dev/ttyAMA0', 57600)
        return panel1

    panel1 = init_panel()


    def setup_drop(segment):

        pos_x = segment + randrange(0, 5)
        pos_y = randrange(-10,40)
        length = randrange(2,8)
        stop_point = randrange(56,64)
        waittostart = 0

        return drop([pos_x, pos_y], length, stop_point, waittostart)





    class drop:
        def __init__(self, pos, length, stop_point, waittostart):
            self.stop_point = stop_point
            self.waitToStart = waittostart
            self.sCount = 0
            self.pos = [pos]
            self.length = length
            self.end = False

        def move(self):
            self.sCount += 1
            if not self.end:
                if self.pos[0][1] < self.stop_point:
                    if self.sCount > self.waitToStart:
                        self.pos.insert(1,self.pos[0][:])
                        if len(self.pos) > self.length:
                            self.pos.pop()
                        self.pos[0][1] += randrange(0, 2)
                elif len(self.pos) > 1:
                    self.pos.pop()
                else:
                    self.pos[0][1] = -1
                    self.end = True




    drops = []
    # Setup each drop in list
    # each drop has a window that it lives in which is the width / number of drops
    for n in range(30):
        segments = 7
        drops.append(setup_drop(56+(n*segments)))

    bottom_drops = []
    for n in range(9):
    	bottom_drops.append([randrange(0,1+n*7),randrange(0,56)])

    while True:

        sleep(.01)

        for i in range(len(drops)):
	    print str(i) + " ",
            print drops[i].pos
	print ""

        panel1._translate()
        panel1.send()
        panel1.clear(0)

        for n, i in enumerate(drops):

            drops[n].move()

            for d, x in enumerate(drops[n].pos):
                x = drops[n].pos[d][1]
                y = drops[n].pos[d][0]
                try:
                    panel1.putpixel([x,y], foreground)
                except:
		    pass
                    #print "error " + str(n)

            if drops[n].end == True:
                segments = 7
                drops[n] = setup_drop(56+(n*segments))

	for n in range(9):
		dice = randrange(0,11)
		if dice == 5:
			bottom_drops[n] = [randrange(0,1+(n*7)),randrange(0,56)]
			try:
				panel1.putpixel(bottom_drops[n], randrange(0,2))
			except:
				pass
		else:
			try:
				panel1.putpixel(bottom_drops[n], 1) 
			except:
				pass
