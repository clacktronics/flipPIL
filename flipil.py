from PIL import Image
import numpy, serial

class flipil:


    def __init__(self, manufacturer, paneldims, arrangement, init_color=0):
        '''

        :param manufacturer: string of the manufacturer so different attributes can be hard set into the class
        :param paneldims: list of each individul module dims [w,h]
        :param arrangement: The arragement of the entire panel

        '''

        self.paneldims = paneldims
        self.arrangement = arrangement
        self.init_color = init_color
        self.portset = False
        self._make_image()

        if manufacturer == "alfa_zeta":
            self.command = []
            for row_n, seg_row in enumerate(arrangement):
                for col_n, seg_col in enumerate(seg_row):
                    self.command.append([0x00] * 32)
                    self.command[row_n][0] = 0x80  # Header
                    self.command[row_n][1] = 0x83  # Mode
		    self.command[row_n][2] = 0x00
                    self.command[row_n][31] = 0x8F  # End
                    self.command[row_n][2] = arrangement[row_n][col_n]  # Panel Addresss

    def _make_image(self):

        # get the largest width of the panel
        prv = 0
        for rw in self.arrangement:
            crt = len(rw)
            if crt > prv:
                self.panels_w = crt
            prv = crt

        self.panels_h = len(self.arrangement)

        self.width = self.panels_w * self.paneldims[0]
        self.height = self.panels_h * self.paneldims[1]

        self._img = Image.new('L', [self.width, self.height], color=self.init_color)

    def set_port(self, port, baud):
        self.serial = serial.Serial(port, baud)
        self.portset = True

    def send(self):
        for message in self.command:
            values = bytearray(message)
            self.serial.write(values)

    def _translate(self):
        img_array = numpy.array(self._img)

        panel_count = 0
        for row_n, panel_row in enumerate(self.arrangement):
            for col_n, panel_col in enumerate(panel_row):

                lower_columb_pixel = col_n*self.paneldims[0]
                upper_columb_pixel = lower_columb_pixel + self.paneldims[0]
                lower_row_pixel = row_n * self.paneldims[1]
                upper_row_pixel = lower_row_pixel + self.paneldims[1]

                #print lower_columb_pixel, upper_columb_pixel
                #print lower_row_pixel, upper_row_pixel

                #render panel
                for x in range(lower_columb_pixel, upper_columb_pixel):
                    output = 0
                    for yn, y in enumerate(range(lower_row_pixel,upper_row_pixel)):
                        bin = 2 ** (yn % 7)
                        if img_array[y][x] == 255:
                            output += bin

                    self.command[panel_count][x+3] = output

                print self.command[panel_count]
                panel_count += 1




    def __getattr__(self,key):
        return getattr(self._img,key)


if __name__ == "__main__":

    from time import sleep    
    refresh = [0x80,0x82,0x8F]

    panel1 = flipil("alfa_zeta", [28, 7], [[1],[2],[3],[4],[5],[6]], init_color = 255)
    panel1.set_port('/dev/ttyAMA0',9600)

    while True:

    	panel1.putpixel([2,3],255)
    	panel1._translate()
	panel1.send()
        panel1.serial.write(refresh)

	sleep(1)
    	panel1.putpixel([2,3],0)
    	panel1._translate()
	panel1.send()
        panel1.serial.write(refresh)
	sleep(1)


