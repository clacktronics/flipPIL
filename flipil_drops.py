from PIL import Image
import numpy
from flipil import flipil
import socket

foreground = 255
background = 0
direction = "down"

# Set up network socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost',1515))

panel_arr = [[8,16,24],[7,15,23],[6,14,22],[5,13,21],[4,12,20],[3,11,19],[2,10,18],[1,9,17]]


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]



    def init_panel():
        panel1 = flipil("alfa_zeta", [28,7], panel_arr, init_color = foreground)
        panel1.set_port('/dev/tty.Bluetooth-Incoming-Port', 57600)
        return panel1

    panel1 = init_panel()

    def sim(image):
        dot = 100
        gap = 5
        img = Image.new("L", (image.size[0]*(dot+gap),image.size[1]*(dot+gap)), color=50)
        drw = ImageDraw.Draw(img)
        for yn, y in enumerate(numpy.array(image).tolist()):
            for xn, x in enumerate(y):
                xpos = xn*(dot+gap)
                ypos = yn*(dot+gap)
                drw.ellipse((xpos, ypos, xpos+dot, ypos+dot), fill=x )
        return img

    def setup_drop(segment):

        pos_x = segment + randrange(0, 5)
        pos_y = randrange(-10,84)
        length = randrange(2,6)
        stop_point = randrange(70,84)
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
    for n in range(10):
        segments = 56 / 10
        drops.append(setup_drop(n*segments))
    p = 0
    ext = False





    while True:
        p = p+1




        #sleep(.5)
        while True:
            m=s.recvfrom(4)
            print m[0]


            if m[0] == "step":
                break
            elif m[0] == "forw":
                direction = "down"
            elif m[0] == "back":
                direction = "up"
            elif m[0] == "bonw":
                foreground = 0
                background = 255
                panel1.clear(background)
                panel1._translate()
                panel1.send()
                print "Black on white set"
            elif m[0] == "wonb":
                foreground = 255
                background = 0
                panel1.clear(background)
                panel1._translate()
                panel1.send()
                print "White on black set"
            elif m[0] == "clear":
                panel1.clear(background)
                panel1._translate()
                panel1.send()


        for i in range(len(drops)):
            print drops[i].pos

        panel1._translate()
        panel1.send()
        panel1.clear(background)

        for n, i in enumerate(drops):

            drops[n].move()


            for d, x in enumerate(drops[n].pos):
                x = drops[n].pos[d][1]
                y = drops[n].pos[d][0]
                try:
                    panel1.putpixel([x,y], foreground)
                except:
                    pass

            if drops[n].end == True:
                segments = 56 / 5
                drops[n] = setup_drop(n*segments)
