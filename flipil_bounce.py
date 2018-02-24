from PIL import Image, ImageDraw
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]

    panel_adds =[
		[0,32],[1,33],[2,34],[3,35],[4,36],[5,37],[6,38],[7,39],
		[8,40],[9,41],[10,42],[11,43],[12,44],[13,45],[14,46],[15,47],
		[16,48],[17,49],[18,50],[19,51],[20,52],[21,53],[22,54],[23,55],
		[24,56],[25,57],[26,58],[27,59],[28,60],[29,61],[30,62],[31,63]
		]

    panel1 = flipil("alfa_zeta", [28, 7], panel_adds, init_color = 0, reverse_panel=False)
    panel1.set_port('/dev/ttyAMA0', 57600)

    def sim(image):
        dot = 8
        gap = 5
        img = Image.new("L", (image.size[0]*(dot+gap),image.size[1]*(dot+gap)), color=50)
        drw = ImageDraw.Draw(img)
        for yn, y in enumerate(numpy.array(image).tolist()):
            for xn, x in enumerate(y):
                xpos = xn*(dot+gap)
                ypos = yn*(dot+gap)
                drw.ellipse((xpos, ypos, xpos+dot, ypos+dot), fill=x )
        return img

	
 
    draw = ImageDraw.Draw(panel1)

    size = 10
    dir_x = 1
    dir_y = 1
    x = 1
    y = 1

    while True:
	#sleep(.01)
        print x, y

	if x+size+2 > panel1.width or x < 1:
            dir_x *= -1
	if y+size+2 > panel1.height or y < 1:
            dir_y *= -1

        x += dir_x
        y += dir_y

        panel1.clear(0)
        draw = ImageDraw.Draw(panel1)
#        draw.text((0,20), "BEN!", fill=1)
        draw.ellipse((x,y,x+size,y+size), outline=1, fill=0)

        panel1._translate()
        panel1.send()


