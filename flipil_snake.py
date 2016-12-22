from PIL import Image, ImageDraw
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    import pygame, os
    from pygame.locals import *
    from PIL import ImageDraw
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

	
  
 
    draw = ImageDraw.Draw(panel1)
    pixel_x = 10
    pixel_y = 10

    import curses
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)

    stdscr.addstr(0,10,"Hit 'q' to quit")
    stdscr.refresh()

    key = ''

    def send_data():  
        panel1.putpixel((old_x, old_y),0)
        panel1.putpixel((pixel_x, pixel_y),1)
        panel1._translate()
        panel1.send()

    while key != ord('q'):

        old_x, old_y = pixel_x, pixel_y

        key = stdscr.getch()
        stdscr.addch(20,25,key)
        stdscr.refresh()
        if key == curses.KEY_LEFT: 
            stdscr.addstr(2, 20, "Up")
            pixel_x -= 1
            send_data()
        elif key == curses.KEY_RIGHT: 
            stdscr.addstr(3, 20, "Down")
            pixel_x += 1
            send_data()
        elif key == curses.KEY_UP: 
            stdscr.addstr(3, 20, "Down")
            pixel_y -= 1
            send_data()
        elif key == curses.KEY_DOWN: 
            stdscr.addstr(3, 20, "Down")
            pixel_y += 1
            send_data()




         


curses.endwin()
