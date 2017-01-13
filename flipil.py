from PIL import Image
import numpy, serial

class flipil:


    def __init__(self, manufacturer, paneldims, arrangement, init_color=0, reverse_panel=False):
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
	self.reverse_panel = reverse_panel

        if manufacturer == "alfa_zeta":
            counter = 0
            self.command = []
            for row_n, seg_row in enumerate(arrangement):
                for col_n, seg_col in enumerate(seg_row):
                    print row_n, col_n, row_n+col_n
                    self.command.append([0x00] * 32)
                    self.command[counter][0] = 0x80  # Header
                    self.command[counter][1] = 0x83  # Mode
                    self.command[counter][2] = arrangement[row_n][col_n]  # Panel Addresss
                    self.command[counter][31] = 0x8F  # End
                    counter += 1

	print self.command

    def clear(self):
        self._img = Image.new('1', [self.width, self.height], color=self.init_color)

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

        self._img = Image.new('1', [self.width, self.height], color=self.init_color)

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

                # Work out upper and lower pixels of this section
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
                        if img_array[y][x] == 1:
                            output += bin

                    #print "Panel count:%d self_command:%d  x:%d x_pos:%d" % (panel_count,len(self.command),x,((x-1%27)+3))

                    # as x is abosulte pixel position of the whole panel we want to make it relative to this panel. 
                    if x > 27:
                        adr = (x-1)%27
                        self.command[panel_count][adr+3] = output
                    else: 
                        self.command[panel_count][x+3] = output

                print panel_count, self.command[panel_count]

		if self.reverse_panel:
			flipped_section = self.command[panel_count][3:31]
			flipped_section.reverse()
			new_command = self.command[panel_count][0:3] + flipped_section + [self.command[panel_count][31]]
			self.command[panel_count] = new_command

                print self.command[panel_count]


                panel_count += 1




    def __getattr__(self,key):
        return getattr(self._img,key)


if __name__ == "__main__":

    from time import sleep    
    refresh = [0x80,0x82,0x8F]

    panel1 = flipil("alfa_zeta", [28, 7], [[1],[2],[3],[4],[5],[6]], init_color = 0)
    panel1.set_port('COM6',9600)

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


