from PIL import Image
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]

    panel1 = flipil("alfa_zeta", [28, 7], [[1],[2],[3],[4],[5],[6]], init_color = 0)
    panel1.set_port('COM6', 57600)

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
        def __init__(self, pos, stop_point, waittostart):
            self.stop_point = stop_point
            self.waitToStart = waittostart
            self.sCount = 0
            self.pos = [pos]
            self.end = False

        def move(self):
            self.sCount += 1
            if not self.end:
                if self.pos[0][0] < self.stop_point:
                    if self.sCount > self.waitToStart:
                        self.pos.insert(1,self.pos[0][:])
                        if len(self.pos) > 20:
                            self.pos.pop()
                        self.pos[0][0] += randrange(0, 2)
                elif len(self.pos) > 1:
                    self.pos.pop()
                else:
                    self.pos[0][0] = 42
                    self.end = True



    drops = []
    for i in range(10):
        segments = 28 / 10
        drops.append(drop([-1,(i*segments) + randrange(0, 5)], randrange(10,42), randrange(20,100)))
    p = 0
    ext = False
    while True:
        p = p+1


        for i in range(len(drops)):
            print drops[i].pos

        print "drops/test%03d.jpg" % p
        sim(panel1._img).save("drops/test%03d.jpg" % p)
        sleep(.5)
        panel1._translate()
        panel1.send()
        panel1.clear()
        if ext:
            break

        ext = True

        for n, i in enumerate(drops):

            drops[n].move()


            for d, x in enumerate(drops[n].pos):
                x = drops[n].pos[d][1]
                y = drops[n].pos[d][0]
                if x < 28:
                    ext = False
                try:
                    panel1.putpixel([x,y], 255)
                except:
                    pass

            if drops[n].end == True:
                segments = 28 / 5
                drops[n] = drop([-1,(n*segments) + randrange(0, 5)], randrange(10,42), n * randrange(20,100))









