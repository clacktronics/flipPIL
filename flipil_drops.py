from PIL import Image
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]

    panel1 = flipil("alfa_zeta", [28,7], [[8,16,24],[7,15,23],[6,14,22],[5,13,21],[4,12,20],[3,11,19],[2,10,18],[1,9,17]], init_color = 0)
    panel1.set_port('/dev/ttyAMA0', 57600)

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
    for i in range(10):
        segments = 56 / 10
        drops.append(drop([(i*segments) + randrange(0, 5),randrange(-10,84)], randrange(2,6),randrange(70,84), 0)) # ([x,y], length, stop_point, waittostart)
    p = 0
    ext = False
    while True:
        p = p+1


        for i in range(len(drops)):
            print drops[i].pos

        #sleep(.5)
        panel1._translate()
        panel1.send()
        panel1.clear()

        for n, i in enumerate(drops):

            drops[n].move()


            for d, x in enumerate(drops[n].pos):
                x = drops[n].pos[d][1]
                y = drops[n].pos[d][0]
                try:
                    panel1.putpixel([x,y], 255)
                except:
                    pass

            if drops[n].end == True:
                segments = 56 / 5
                drops[n] = drop([(n*segments) + randrange(0, 5),randrange(-10,84)], randrange(2,6),randrange(70,84), 0) # ([x,y], length, stop_point, waittostart)









