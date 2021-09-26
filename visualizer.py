import os
import sys
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.axes as Axes
import numpy as np


class GLines :
    xVal = 0
    yVal = 0
    zVal = 0
    moveType = 0
    gLine = []
    isG0G1 = False
    isPenDown = False
    command = ''
    update = [0,0,0] # [x,y,z]

    def __init__(self):
        self.update = [0,0,0]

    def readline(self, gline):
        print(gline)
        self.gLine = gline.split()
        self.update = [0,0,0]

    def getPos(self, sx =0, sy =0, sz =0):

        if len(self.gLine) < 1:
            print("No Entry")

        elif self.gLine[0]== 'G0' or self.gLine[0] == 'G1':

            self.isG0G1 = True
            print(' Length of command : %d ' %( len(self.gLine) ))

            dr = [0,0]
            for term in self.gLine:
                if term[0] == ';':
                    break
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



            # Move Type is only defined by  first 3 bits (x,y,z)
            # if only x,y move , it will be 011 , which is 3
            # if only z move , it will be 100 , which is 4
            out = 0
            for bit in reversed(self.update) :
                out = ( out << 1 ) | bit

            # 7 is 111 in binary
            self.moveType = out & 7
    
    def getCommand(self):

        if len(self.gLine) < 1:
            print("No Entry")

        elif self.gLine[0][0] != ';':
            self.command = self.gLine[0]

        elif self.gLine[0][0] == ';':
            self.command = 'Comment'
            self.description = ' '.join(self.gLine)

    def posUpdated(self):

        move = False
        if sum(self.update[:2]) > 0 :
            move = True

        return move
    
    def getPenDown(self):
        val = self.isPenDown
        print(val)
        return val


def main(gui, gcode_file_path):
    gcode_file = open(gcode_file_path)
    gcode_lines = gcode_file.readlines()
    print("lines: ",len(gcode_lines))
    gd = GLines()

    fig, ax = plt.subplots(figsize=(12, 6))

    plt.xlim([0, 250])
    plt.ylim([0, 150])

    strokeData = []

    for line in gcode_lines:
        #print(line, end='')

        if len(line) < 1 :
            print( ' line size = ' + str( len(line)) )
            continue

        # Read line from the file
        gd.readline(line)
        # Get command ( G, M or ... )
        gd.getCommand()
        cmd = gd.command
        # Get X Y Z E F
        gd.getPos()

        if cmd == 'G28':
            print(' Home - Initialized ' + cmd +' \n')
            v.append([0, 0, 0])

        # if one of x,y,z moved
        if  gd.posUpdated() and gd.getPenDown():

            # Record each position and motion type with its color code
            strokeData.append( [gd.xVal, gd.yVal] )
        elif not gd.getPenDown():
            #if the end of a stroke is reached (ie the pen is raised), end the previous stroke and create a new one
            print(strokeData)
            x = np.asarray([coord[0] for coord in strokeData])
            y = np.asarray([150 + coord[1] for coord in strokeData])
    
            ax.plot(x, y, linestyle='-')

            strokeData = []

    gcode_file.close()
    #print(v)
    x = np.asarray([coord[0] for coord in strokeData])
    y = np.asarray([150 + coord[1] for coord in strokeData])
    
    ax.plot(x, y, linestyle='-')
    plt.show()

if __name__ == '__main__':

    import argparse

    visualizer_parser = argparse.ArgumentParser()

    visualizer_parser.add_argument('--nogui', default=False, action="store_true")
    visualizer_parser.add_argument("gcode_file_path", type=str, help="Path to G-Code file you would like visualized")

    args = visualizer_parser.parse_args()
    gui = args.nogui
    gcode_file_path = args.gcode_file_path

    if not os.path.isfile(gcode_file_path):
        print("The G-code instruction file specified does not exist on this path.")
        sys.exit()

    main(gui, gcode_file_path)