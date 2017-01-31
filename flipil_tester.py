from PIL import Image
import numpy
from flipil import flipil


if __name__ == "__main__":



    from time import sleep
    from PIL import ImageDraw
    from random import randrange
    refresh = [0x80,0x82,0x8F]


    for i in range(10):
        panel1 = flipil("alfa_zeta", [28,7], [[8,16,24],[7,15,23],[6,14,22],[5,13,21],[4,12,20],[3,11,19],[2,10,18],[1,9,17]], init_color = 1)
        panel1.set_port('/dev/ttyAMA0', 57600)
        panel1._translate()
        panel1.send()
        panel1.clear()

        panel1 = flipil("alfa_zeta", [28,7], [[8,16,24],[7,15,23],[6,14,22],[5,13,21],[4,12,20],[3,11,19],[2,10,18],[1,9,17]], init_color = 0)
        panel1.set_port('/dev/ttyAMA0', 57600)
        panel1._translate()
        panel1.send()
        panel1.clear()









