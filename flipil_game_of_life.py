from PIL import Image, ImageDraw
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw, Image
    from random import randrange
    refresh = [0x80,0x82,0x8F]

    panel1 = flipil("alfa_zeta", [28, 7], [[1],[2],[3],[4],[5],[6]], init_color = 0)
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

	
    im = Image.new("1",(42,28), color=0)
    drw = ImageDraw.Draw(im)
    drw.text((0,0),"Game Of", fill=1)
    drw.text((10,10),"Life", fill=1)
    im = im.rotate(90, expand=1)
    panel1.paste(im) 

    #draw = ImageDraw.Draw(panel1)
    #draw.ellipse((10,10,20,30), outline=1, fill=0)
    #draw.rectangle((0,30,10,35), outline=1, fill=1)
#    draw.line((20,10,22,10), width=1, fill=1)
    panel1._translate()
    panel1.send()
    sleep(5)
    while True:

        panel1._translate()
        panel1.send()
        #panel1.clear()


        output = []
	for pixel_x in range(panel1.width):
            for pixel_y in range(panel1.height):

                positions = ['nn', 'ne', 'ee', 'se', 'ss', 'sw', 'ww', 'nw']

                if pixel_x == 0: positions = [x for x in positions if x not in ['sw','ww','nw']]
                elif pixel_x == panel1.width-1: positions = [x for x in positions if x not in ['ne','ee','se']]
                if pixel_y == 0: positions = [x for x in positions if x not in ['nn','ne','nw']]
                elif pixel_y == panel1.height-1: positions = [x for x in positions if x not in ['se','ss','sw']]

		GOL = {'alive':panel1.getpixel((pixel_x,pixel_y))}

		for dir in positions:
                    if dir == 'nn': GOL['nn'] = panel1.getpixel((pixel_x  ,pixel_y-1))
                    elif dir == 'ne': GOL['ne'] = panel1.getpixel((pixel_x+1,pixel_y-1))
                    elif dir == 'ee': GOL['ee'] = panel1.getpixel((pixel_x+1,pixel_y  ))
                    elif dir == 'se': GOL['se'] = panel1.getpixel((pixel_x+1,pixel_y+1))
                    elif dir == 'ss': GOL['ss'] = panel1.getpixel((pixel_x  ,pixel_y+1))
                    elif dir == 'sw': GOL['sw'] = panel1.getpixel((pixel_x-1,pixel_y+1))
                    elif dir == 'ww': GOL['ww'] = panel1.getpixel((pixel_x-1,pixel_y  ))
                    elif dir == 'nw': GOL['nw'] = panel1.getpixel((pixel_x-1,pixel_y-1))
                
                population_count = 0
                for location in GOL:
                    if location is not 'alive':         #only look at other squares
                        population_count+=GOL[location] # add the value as if 0 it will do nothing anyway

#		print pixel_x, pixel_y, GOL, population_count, 

                if GOL['alive']==1: # If alive
                    if population_count < 2 or population_count > 3: 
                        #panel1.putpixel((pixel_x,pixel_y),0)
                        output.append([pixel_x, pixel_y, 0])
                else: # If dead
                    if population_count == 3:
			#panel1.putpixel((pixel_x,pixel_y),1)
                        output.append([pixel_x, pixel_y, 1])


              
        for ip, p in enumerate(output):
            panel1.putpixel((output[ip][0], output[ip][1]),output[ip][2])

	print 'boop'









