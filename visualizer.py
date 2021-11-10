import os
import sys
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.axes as Axes
import numpy as np
from PIL import Image, ImageDraw


class GLines :
    xVal = 0
    yVal = 0
    zVal = 0
    moveType = 0
    gLine = []
    isG0G1 = False
    isPenDown = False
    penColor = ""
    command = ''
    update = [0,0,0] # [x,y,z]
    drawingType = ""

    def __init__(self, drawingType):
        self.update = [0,0,0]
        self.penColor = "none"
        self.drawingType = drawingType

    def readline(self, gline):
        verboseprint(gline)
        self.gLine = gline.split()
        self.update = [0,0,0]

    def getPos(self, resolution):
        selfx = self.xVal
        selfy = self.yVal
        return ((resolution*selfx, resolution*(150+selfy)))
    
    def updatePos(self, sx=0, sy=0, sz=0):
        if len(self.gLine) < 1:
            verboseprint("No Entry")

        elif self.gLine[0]== 'G0' or self.gLine[0] == 'G1':

            self.isG0G1 = True
            verboseprint(' Length of command : %d ' %( len(self.gLine) ))

            for term in self.gLine:
                if term[0] == 'X':
                    iVal = float(term[1:])
                    if iVal != self.xVal:
                        self.xVal = iVal + sx
                        self.update[0] = 1
                if term[0] == 'Y':
                    iVal = float( term[1:])
                    if iVal != self.yVal:
                        self.yVal = iVal + sy
                        self.update[1] = 1
                if term[0] == 'Z':
                    iVal = float(term[1:])
                    if iVal != self.zVal:
                        self.zVal = iVal + sz
                        self.update[2] = 1
                    if iVal == 0:
                        self.isPenDown = True
                    elif iVal != 0:
                        self.isPenDown = False
             
    def getCommand(self):

        if len(self.gLine) < 1:
            verboseprint("No Entry")

        elif self.gLine[0][0] != ';':
            # print(self.gLine)
            self.command = self.gLine[0]
            self.updatePos()

        elif self.gLine[0][0] == ';':
            self.command = 'Color change'
            verboseprint(self.command)
            self.description = ' '.join(self.gLine)
            self.updateColor()

        return self.command

    def posUpdated(self):
        move = False
        if sum(self.update[:2]) > 0 :
            move = True
        return move
    
    def getPenDown(self):
        val = self.isPenDown
        verboseprint(val)
        return val

    def getColor(self):
        color = self.penColor
        artType = self.drawingType
        
        possible_colors = dict()
        possible_colors['brown'] = [102, 82, 86]
        possible_colors['blue'] = [78, 151, 228]
        possible_colors['yellow'] = [249, 216, 36]
        possible_colors['orange'] = [238, 75, 29]
        possible_colors['green'] = [56, 131, 57]
        possible_colors['red'] = [171, 24, 26]
        possible_colors['purple'] = [54, 35, 88]
        possible_colors['black'] = [31, 25, 33]
        possible_colors['none'] = [0, 0, 0]
        
        ret = possible_colors[color]
        ret.append(int(0.3*255))

        if artType == "watercolor":
            return tuple(ret)
        else:
            return tuple(possible_colors[color])

    def updateColor(self):
        # possible_colors = {"brown": [102, 82, 86], "lightblue": [78, 151, 228], "yellow": [249, 216, 36], "orange": [238, 75, 29], "green": [56, 131, 57], "red": [171, 24, 26], "purple": [54, 35, 88], "black": [31, 25, 33]}
        line = self.gLine
        for i in line:
            if i.strip() != ";" and i.strip() != " ":
                color = i
        if not color:
            return
        if self.penColor != color:
            self.penColor = color
            print("Changing pen color to %s" % self.penColor)


def main(gcode_file_path, color, artType, resolution):
    gcode_file = open(gcode_file_path)
    gcode_lines = gcode_file.readlines()
    verboseprint("lines: ",len(gcode_lines))
    gd = GLines(artType)

    xRatio = 18/30
    yDim = 150 * resolution
    xDim = int(yDim * xRatio)
    imgDim = (xDim, yDim)

    if artType == "watercolor":
        width = 4 * resolution
    else:
        width = resolution
    
    image = Image.new(mode = "RGB", size = imgDim, color=(255, 255, 255))
    print(image)
    if artType == "watercolor":
        draw = ImageDraw.Draw(image, "RGBA")
    else:
        draw = ImageDraw.Draw(image)

    # plt.xlim([0, 250])
    # plt.ylim([0, 150])

    strokeData = []

    for line in gcode_lines:
        #print(line, end='')

        if len(line) < 1 :
            verboseprint( ' line size = ' + str( len(line)) )
            continue

        # Read line from the file
        gd.readline(line)
        # Get command ( G, M or ... )
        cmd = gd.getCommand()
        
        if cmd == 'G28':
            verboseprint(' Home - Initialized ' + cmd +' \n')
            strokeData.append([0, 0])

        # if one of x,y,z moved
        if  gd.posUpdated() and gd.getPenDown():
            # Record each position
            strokeData.append(gd.getPos(resolution))
        elif not gd.getPenDown():
            #if the end of a stroke is reached (ie the pen is raised), end the previous stroke and create a new one
            #print(strokeData)
            
            draw.line(strokeData, fill=gd.getColor(), joint=None, width=width)

            strokeData = []

    gcode_file.close()
    #print(v)
    draw.line(strokeData, fill=gd.getColor(), joint=None, width=width)

    image.show()

if __name__ == '__main__':

    import argparse

    visualizer_parser = argparse.ArgumentParser()

    visualizer_parser.add_argument("--usecolor", default=False, action="store_true", help="Colors for various lines are stored in parenthetical comments... if this flag is provided, these colors should be used in visualization")
    visualizer_parser.add_argument("-v", default=False, action="store_true", help="Print debug statements")
    visualizer_parser.add_argument("gcode_file_path", type=str, help="Path to G-Code file you would like visualized")
    visualizer_parser.add_argument("artType", type=str, help="String indicating type of art the visualizer should render (choices: pen, watercolor)")
    visualizer_parser.add_argument("resolution", type=int, help="conversion factor between millimeters declared in G-code and pixel resolution")

    args = visualizer_parser.parse_args()
    color = args.usecolor
    verbose = args.v
    gcode_file_path = args.gcode_file_path
    artType = args.artType
    resolution = args.resolution

    if verbose:
        def verboseprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
            for arg in args:
                print(arg)
            print
    else:   
        verboseprint = lambda *a: None      # do-nothing function

    if not os.path.isfile(gcode_file_path):
        print("The G-code instruction file specified does not exist on this path.")
        sys.exit()

    if not artType in ["watercolor", "pen"]:
        raise ValueError("Invalid type of art given: current choices are watercolor and pen")

    main(gcode_file_path, color, artType, resolution)