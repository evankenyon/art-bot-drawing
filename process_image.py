#!/usr/bin/env python
# coding: utf-8

# In[102]:

# all this code was borrowed from 
# https://towardsdatascience.com/how-i-used-machine-learning-to-automatically-hand-draw-any-picture-7d024d0de997
from typing import OrderedDict
import cv2;
from matplotlib import pyplot as plt
import numpy as np
import pyautogui as pg
import kdtree
import operator
from Paint_CNC import Paint_CNC
from cnc import CNC
from sklearn.cluster import KMeans
from collections import defaultdict
import os, sys, time
from grid import Grid

class AutoDraw(object):
    def __init__(self, name, blur = 0, xDim=None, yDim=None):
        # Tunable parameters
        self.detail = 1
#         self.scale = 7/12
        self.scale = 1
        self.sketch_before = False
        self.with_color = True
        self.num_colors = 10
        self.outline_again = False
        self.possible_colors = OrderedDict()
        self.possible_colors['brown'] = [102, 82, 86]
        self.possible_colors['blue'] = [78, 151, 228]
        self.possible_colors['yellow'] = [249, 216, 36]
        self.possible_colors['orange'] = [238, 75, 29]
        self.possible_colors['green'] = [56, 131, 57]
        self.possible_colors['red'] = [171, 24, 26]
        self.possible_colors['purple'] = [54, 35, 88]
        self.possible_colors['black'] = [31, 25, 33]
        # Load Image. Switch axes to match computer screen
        self.img = cv2.imread(name)
        self.blur = blur
        self.img = np.swapaxes(self.img, 0, 1)
        self.img_shape = self.img.shape

#         self.dim = pg.size()

        # 30 cm x 18 cm
        if xDim == None and yDim == None:
            self.xRatio = 18/30
            self.yDim = 150
            self.xDim = self.yDim * self.xRatio
        else:
            self.xDim = xDim
            self.yDim = yDim
        self.dim = (self.yDim, self.xDim)
        # Scale to draw inside part of screen
        self.startX = ((1 - self.scale) / 2)*self.dim[0] 
        self.startY = ((1 - self.scale) / 2)*self.dim[1]
#         self.dim = (self.dim[0] * self.scale, self.dim[1] * self.scale)

#         fit the picture into this section of the screen
        # if self.img_shape[1] > self.img_shape[0]:
        #     # if it's taller that it is wide, truncate the wide section
        #     self.dim = (int(self.dim[1] * (self.img_shape[0] / self.img_shape[1])), self.dim[1])
        # else:
        #     # if it's wider than it is tall, truncate the tall section
        #     self.dim = (self.dim[0], int(self.dim[0] *(self.img_shape[1] / self.img_shape[0])))

        # Get dimension to translate picture. Dimension 1 and 0 are switched due to comp dimensions
        ratio = self.img.shape[0] / self.img.shape[1]
        pseudo_x = int(self.img.shape[1] * self.detail)
        self.pseudoDim = (pseudo_x, int(pseudo_x * ratio))

# Tunable parameters
        # self.detail = 1
        # self.scale = 7/12
        # self.sketch_before = False
        # self.with_color = True
        # self.num_colors = 10
        # self.outline_again = False

        # # Load Image. Switch axes to match computer screen
        # self.img = cv2.imread(name)
        # self.blur = blur
        # self.img = np.swapaxes(self.img, 0, 1)
        # self.img_shape = self.img.shape

        # self.dim = pg.size()

        # # Scale to draw inside part of screen
        # self.startX = ((1 - self.scale) / 2)*self.dim[0] 
        # self.startY = ((1 - self.scale) / 2)*self.dim[1] 
        # self.dim = (self.dim[0] * self.scale, self.dim[1] * self.scale)

        # # fit the picture into this section of the screen
        # if self.img_shape[1] > self.img_shape[0]:
        #     # if it's taller that it is wide, truncate the wide section
        #     self.dim = (int(self.dim[1] * (self.img_shape[0] / self.img_shape[1])), self.dim[1])
        # else:
        #     # if it's wider than it is tall, truncate the tall section
        #     self.dim = (self.dim[0], int(self.dim[0] *(self.img_shape[1] / self.img_shape[0])))

        # # Get dimension to translate picture. Dimension 1 and 0 are switched due to comp dimensions
        # ratio = self.img.shape[0] / self.img.shape[1]
        # pseudo_x = int(self.img.shape[1] * self.detail)
        # self.pseudoDim = (pseudo_x, int(pseudo_x * ratio))
        
          # Initialize directions for momentum when creating path
        self.maps = {0: (1, 1), 1: (1, 0), 2: (1, -1), 3: (0, -1), 4: (0, 1), 5: (-1, -1), 6: (-1, 0), 7: (-1, 1)}
        self.momentum = 1
        self.curr_delta = self.maps[self.momentum]

        # Create Outline
        self.drawing = self.process_img(self.img)
        # plt.imshow(self.drawing)
        # plt.show()

    def rescale(self, img, dim):
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    def translate(self, coord):
        ratio = (coord[0] / self.pseudoDim[1], coord[1] / self.pseudoDim[0]) # this is correct
        deltas = (int(ratio[0] * self.dim[0]), int(ratio[1] * self.dim[1]))
        return self.startX + deltas[0], self.startY + deltas[1]
    
    def process_img(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.blur == 2:
            gray = cv2.GaussianBlur(gray, (9, 9), 0)
            canny = cv2.Canny(gray, 25, 45)
        elif self.blur == 1:
            gray = cv2.GaussianBlur(gray, (3, 3), 0)
            canny = cv2.Canny(gray, 25, 45)
        else:  # no blur
            canny = cv2.Canny(gray, 50, 75)
        canny = self.rescale(canny, self.pseudoDim)
        r, res = cv2.threshold(canny, 50, 255, cv2.THRESH_BINARY_INV)

        return res
    
    def drawOutline(self):
        indices = np.argwhere(self.drawing < 127).tolist()  # get the black colors
        index_tuples = map(tuple, indices)

        self.hashSet = set(index_tuples)
        self.KDTree = kdtree.create(indices)
#         self.KDTree = KDTree(indices)
        self.commands = []
        self.curr_pos = (0, 0)
        point = self.translate(self.curr_pos)
        self.commands.append(point)

#         print('Please change pen to thin and color to black.')
#         input("Press enter once ready")
#         print('')

        # DRAW THE BLACK OUTLINE
        self.createPath()
#         self.cleanCommands()
        return self.commands
#         print(self.commands)
#         input("Ready! Press Enter to draw")
#         print('5 seconds until drawing beings')
#         time.sleep(5)

#         self.execute(self.commands)

    def execute(self, commands):
        press = 0  # flag indicating whether we are putting pressure on paper
    
        for (i, comm) in enumerate(commands):
            if type(comm) == str:
                if comm == 'UP':
                    press = 0
                if comm == 'DOWN':
                    press = 1
            else:
                print(len(commands) - i)
                if press == 0:
                    pg.moveTo(comm[0], comm[1], 0)
                else:
                    pg.dragTo(comm[0], comm[1], 0, button='left')
        return

    def createPath(self):
        # check for closest point. Go there. Add click down. Change curr. Remove from set and tree. Then, begin
        new_pos = tuple(self.KDTree.search_nn(self.curr_pos)[0].data)
#         print(self.curr_pos[0)
#         new_pos = tuple(self.KDTree.query(self.curr_pos)[0].data)
        self.commands.append(new_pos)
        self.commands.append("DOWN")
        self.curr_pos = new_pos
        self.KDTree = self.KDTree.remove(list(new_pos))
        self.hashSet.remove(new_pos)

        while len(self.hashSet) > 0:
            prev_direction = self.momentum
            candidate = self.checkMomentum(self.curr_pos)
            if self.isValid(candidate):
                new = tuple(map(operator.add, self.curr_pos, candidate))
                new_pos = self.translate(new)
                if prev_direction == self.momentum and type(self.commands[-1]) != str:  # the direction didn't change
                    self.commands.pop()
                self.commands.append(new_pos)
            else:
                self.commands.append("UP")
                new = tuple(self.KDTree.search_nn(self.curr_pos)[0].data)
#                 new = tuple(self.KDTree.query(self.curr_pos)[0].data)
                new_pos = self.translate(new)
                self.commands.append(new_pos)
                self.commands.append("DOWN")
            self.curr_pos = new
            self.KDTree = self.KDTree.remove(list(new))
            self.hashSet.remove(new)
            # print('Just went to point ', self.curr_pos)
            # print('Making path...number points left: ', len(self.hashSet))
        return self.commands

#     def cleanCommands(self):
#         self.commands = self.commands[2:]
#         for command in self.commands:
#             if(type(command) is not str):
#                 command[0] -= 25
#                 command[1] -=25

    def isValid(self, delta):
        return len(delta) == 2

    def checkMomentum(self, point):
        # Returns best next relative move w.r.t. momentum and if in hashset
        self.curr_delta = self.maps[self.momentum]
        moments = self.maps.values()
        deltas = [d for d in moments if (tuple(map(operator.add, point, d)) in self.hashSet)]
        deltas.sort(key=self.checkDirection, reverse=True)
        if len(deltas) > 0:
            best = deltas[0]
            self.momentum = [item[0] for item in self.maps.items() if item[1] == best][0]
            return best
        return [-1]

    def checkDirection(self, element):
        return self.dot(self.curr_delta, element)

    def dot(self, pt1, pt2):
        pt1 = self.unit(pt1)
        pt2 = self.unit(pt2)
        return pt1[0] * pt2[0] + pt1[1] * pt2[1]

    def unit(self, point):
        norm = (point[0] ** 2 + point[1] ** 2)
        norm = np.sqrt(norm)
        return point[0] / norm, point[1] / norm
    
    def get_line_color(self, r, g, b):
        
        min_distance = 9999999999
        min_color = ""
        for color, rgb in self.possible_colors.items():
            possible_min_distance = abs(r - rgb[0]) + abs(g - rgb[1]) + abs(b - rgb[2])
            if possible_min_distance < min_distance:
                min_distance = possible_min_distance
                min_color = color
        return min_color


    def draw(self):
        if self.with_color:
            # Original:
            # color = self.rescale(self.img, self.pseudoDim)
            # collapsed = np.sum(color, axis=2)/3
            # fill = np.argwhere(collapsed < 230)  # color 2-d indices
            # fill = np.swapaxes(fill, 0, 1)  # swap to index into color
            # RGB = color[fill[0], fill[1], :]
            # k_means = KMeans(n_clusters=self.num_colors).fit(RGB)
            # colors = k_means.cluster_centers_
            # labels = k_means.labels_
            # fill = np.swapaxes(fill, 0, 1).tolist()  # swap back to make dictionary
            # label_2_index = defaultdict(list)

            # for i, j in zip(labels, fill):
            #     label_2_index[i].append(j)
            # print(label_2_index)


            color = self.rescale(self.img, self.pseudoDim)
            collapsed = np.sum(color, axis=2)/3
            fill = np.argwhere(collapsed < 230)  # color 2-d indices
            fill = np.swapaxes(fill, 0, 1)  # swap to index into color
            RGB = color[fill[0], fill[1], :]
            colors = self.possible_colors.values()

            color_commands = OrderedDict()
            color_commands['brown'] = []
            color_commands['blue'] = []
            color_commands['yellow'] = []
            color_commands['orange'] = []
            color_commands['green'] = []
            color_commands['red'] = []
            color_commands['purple'] = []
            color_commands['black'] = []
            labels = []

            for (i, color) in enumerate(RGB):
                line_color = self.get_line_color(color[2], color[1], color[0])
                labels.append(list(color_commands.keys()).index(line_color))

            fill = np.swapaxes(fill, 0, 1).tolist()  # swap back to make dictionary
            
            label_2_index = defaultdict(list)
            for i, j in zip(labels, fill):
                label_2_index[i].append(j)
            
            for (i, color) in enumerate(colors):
                if label_2_index[i] == []:
                    continue

                # Grayscale conversion formula found at 
                # https://www.dynamsoft.com/blog/insights/image-processing/image-processing-101-color-space-conversion/
                # grayscale = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
#                 print(grayscale)
                # print('Please change the pen to thick and color to BGR (not RGB) values: ', color)
                # input("Press enter once ready")
                # print('')
                points = label_2_index[i]
                index_tuples = map(tuple, points)
                self.hashSet = set(index_tuples)
                self.KDTree = kdtree.create(points)
                self.commands = []
                self.curr_pos = (0, 0)
                point = self.translate(self.curr_pos)
                self.commands.append("UP")
                self.commands.append(point)

                line_color = self.get_line_color(color[0], color[1], color[2])
                self.commands.append(line_color)
                # if(color[2] >= color[1] and color[2] >= color[0]):
                #     line_color = "red"
                #     print("red")
                #     # self.commands.append("BLUE")
                # if(color[1] >= color[2] and color[1] >= color[0]):
                #     line_color = "green"
                #     print("green")
                #     # self.commands.append("GREEN")
                # if(color[0] >= color[2] and color[0] >= color[1]):
                #     line_color = "blue"
                #     print("blue")
                #     # self.commands.append("RED")
                # if (max(color) <= 50):
                #     line_color = "black"
                color_commands[line_color] += self.createPath()
                self.commands.append("UP")

                # input('Ready! Press enter to draw: ')
                # print('5 seconds until drawing begins...')
                # time.sleep(5)
                # try: 
                # self.execute(self.commands)
                # except KeyboardInterrupt:
                #     sys.exit()
            
            return color_commands
            # return self.commands
            if self.outline_again:
                self.drawOutline()


# In[62]:

    def commands_to_cnc(self, cnc, commands, prevNonUpOrDownCommand, color, pen_color=False):
        newCommands = [] 
        for index in range(len(commands)):
            if(prevNonUpOrDownCommand == commands[index]):
                continue
            if commands[index] == 'UP':
                if index + 1 == len(commands):
                    newCommands.append(commands[index])
                elif commands[index + 1] != 'UP' and commands[index + 1] != 'DOWN':
                    newCommands.append(commands[index])
    #               cnc.up()
            elif commands[index] == 'DOWN':
                if index + 1 == len(commands):
                    newCommands.append(commands[index])
                elif commands[index + 1] != 'UP' and commands[index + 1] != 'DOWN':
                    newCommands.append(commands[index])
            else:
                newCommands.append(commands[index])
                prevNonUpOrDownCommand = commands[index]

        preCondensedCommands = []

        for index in range(len(newCommands)):
            if newCommands[index] == color:
                preCondensedCommands.append(color)
                # cnc.set_paint_color(color)
            elif newCommands[index] == None:
                continue
            elif newCommands[index] == 'UP' or newCommands[index - 1] == color:
                if index + 1 == len(newCommands):
                    preCondensedCommands.append('UP')
                    # cnc.up()
                elif newCommands[index + 1] != 'UP' and newCommands[index + 1] != 'DOWN':
                    preCondensedCommands.append('UP')
                    # cnc.up()
            elif newCommands[index] == 'DOWN':
                if newCommands[index - 2] == color:
                    preCondensedCommands.append('UP')
                    # cnc.g1(z=5)
                elif index + 1 == len(newCommands):
                    preCondensedCommands.append('DOWN')
                    # cnc.down()
                elif newCommands[index + 1] != 'UP' and newCommands[index + 1] != 'DOWN':
                    preCondensedCommands.append('DOWN')
                    # cnc.down()
            else:
                # print(newCommands[index])
                # print(newCommands[index])
                if newCommands[index - 4] == color:
                    preCondensedCommands.append('DOWN')
                    # cnc.down()
                preCondensedCommands.append((float(newCommands[index][1]), -float(newCommands[index][0])))
                # cnc.g1(x=float(newCommands[index][1]),y=-float(newCommands[index][0]))

        realPreCondensedCommands = []
        
        isUp = False
        prevCommand = None
        for command in preCondensedCommands:
            if command == color:
                realPreCondensedCommands.append(color)
            if command == 'UP':
                if not isUp:
                    realPreCondensedCommands.append('UP')
                isUp = True
            elif command == 'DOWN':
                if isUp:
                    realPreCondensedCommands.append(prevCommand)
                    realPreCondensedCommands.append('DOWN')
                    isUp = False
            else:
                if not isUp:
                    realPreCondensedCommands.append(command)
                prevCommand = command

        
        if color == "NA":
            for command in realPreCondensedCommands:
                if command == color:
                    continue
                elif command == 'UP':
                    cnc.up()
                elif command == 'DOWN':
                    cnc.down()
                else:
                    cnc.g0(x=command[0], y=command[1])
            return realPreCondensedCommands
        elif pen_color:
            for command in realPreCondensedCommands:
                if command == color:
                    cnc.comment(color)
                elif command == 'UP':
                    cnc.up()
                elif command == 'DOWN':
                    cnc.down()
                else:
                    cnc.g0(x=command[0], y=command[1])
            return realPreCondensedCommands
        else:
            condensedCommands = []
            grid = Grid(self.xDim, -self.yDim)
            isUp = False
            print(len(realPreCondensedCommands))
            count = 0
            for index in range(len(realPreCondensedCommands)):
                count += 1
                print(count)
                if realPreCondensedCommands[index] == color:
                    condensedCommands.append(color)
                elif realPreCondensedCommands[index] == 'UP':
                    condensedCommands.append('UP')
                    isUp = True
                elif realPreCondensedCommands[index] == 'DOWN':
                    condensedCommands.append('DOWN')
                    isUp = False
                elif index + 1 >= len(realPreCondensedCommands):
                    continue
                elif realPreCondensedCommands[index + 1]  == color or realPreCondensedCommands[index + 1]  == 'UP' or realPreCondensedCommands[index + 1]  == 'DOWN':
                    if not isUp:
                        if(grid.shouldAdd(realPreCondensedCommands[index][0], realPreCondensedCommands[index][1])):
                            condensedCommands.append(realPreCondensedCommands[index])
                    if isUp: 
                        condensedCommands.append(realPreCondensedCommands[index])
                    # continue
                else:
                    if isUp:
                        condensedCommands.append(realPreCondensedCommands[index])
                    if not isUp:
                        condensedCommands.extend(grid.getParsedCommands(realPreCondensedCommands[index][0], realPreCondensedCommands[index][1], realPreCondensedCommands[index + 1][0], realPreCondensedCommands[index + 1][1]))


            # print(condensedCommands)

            prevCommand = (-1000, 1000)
            isUp = False
            count = 0
            for command in condensedCommands:
                count += 1
                if command == color:
                    prevCommand = command
                    cnc.set_paint_color(color)
                elif command == 'UP':
                    isUp = True
                    prevCommand = command
                    cnc.up()
                elif command == 'DOWN':
                    isUp = False
                    if prevCommand != 'DOWN' and prevCommand != 'UP' and prevCommand != color:
                        cnc.g0(x=prevCommand[0], y=prevCommand[1])
                    prevCommand = command
                    cnc.down()
                else:
                    if command != prevCommand and not isUp:
                        cnc.g0(x=command[0], y=command[1])
                    prevCommand = command

            return condensedCommands

def main(image_file_path, gcode_file_path, with_color, pen_color, blur=0, xDim=None, yDim=None):
    print(pen_color)
    drawing = AutoDraw(image_file_path, blur=blur, xDim=xDim, yDim=yDim)
    if with_color or pen_color:
        color_commands = drawing.draw()
    else:
        commands = drawing.drawOutline()
    # commands += drawing.drawOutline()
    
    
    # cnc.g1(z=0)
    prevNonUpOrDownCommand = (0, 0)
    newCommands = [] 
    
    if pen_color:
        cnc = CNC()
        cnc.open(gcode_file_path)

        cnc.g90()
        cnc.g0(z=5)
        cnc.f(3000)
        cnc.g0(z=5)
        for color in color_commands:
            if color_commands[color]:
                cnc.comment(color)
                commands = color_commands[color]
                newCommands.extend(drawing.commands_to_cnc(cnc, commands, prevNonUpOrDownCommand, color, pen_color=True))
    elif not with_color:
        cnc = CNC()
        cnc.open(gcode_file_path)

        cnc.g90()
        cnc.g0(z=5)
        cnc.f(3000)
        cnc.g0(z=5)
        newCommands = drawing.commands_to_cnc(cnc, commands, prevNonUpOrDownCommand, "NA")
    else:
        cnc = Paint_CNC()
        cnc.open(gcode_file_path)

        cnc.g90()
        cnc.g0(z=5)
        cnc.f(3000)
        cnc.g0(z=5)
        for color in color_commands:
            if color_commands[color]:
                cnc.comment(color)
                commands = color_commands[color]
                newCommands.extend(drawing.commands_to_cnc(cnc, commands, prevNonUpOrDownCommand, color))
    
    cnc.close()

# In[ ]:

if __name__ == "__main__":
    import argparse

    process_parser = argparse.ArgumentParser()

    process_parser.add_argument('image_file_path', type=str, help="Path to image file you would like turned into G-Code")
    process_parser.add_argument("gcode_file_path", type=str, help="Path to where you want the G-Code file to be saved")
    # process_parser.add_argument("with_color", type=int, help="True for with color, false for without")
    process_parser.add_argument("blur", nargs="?", type=int, help="Amount of blur for image (between 0 and 2)")
    process_parser.add_argument("xDim", nargs="?", type=float, help="x dimension in mm")
    process_parser.add_argument("yDim", nargs="?", type=float, help="y  dimension in mm")
    process_parser.add_argument("--usecolor", default=False, action="store_true", help="If this flag is provided, we want the image to be used with watercolors")
    process_parser.add_argument("--pencolor", default=False, action="store_true", help="If this flag is provided, we want the image to be with pen but in color")

    args = process_parser.parse_args()
    image_file_path = args.image_file_path
    gcode_file_path = args.gcode_file_path
    with_color = args.usecolor
    pen_color = args.pencolor
    xDim = args.xDim
    yDim = args.yDim
    blur = args.blur

    if not os.path.isfile(image_file_path):
        print("The reference image file specified does not exist on this path.")
        sys.exit()
    main(image_file_path, gcode_file_path, with_color, pen_color, blur, xDim, yDim)

