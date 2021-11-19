import math

from grid_location import GridLocation


class Grid(object):

    def __init__(self, xDim, yDim):
        self.xDim = xDim
        self.yDim = yDim
        self.allLines = []
        self.gridLocations = []
        self.size = 0.1
        self.range = 2
        self.isUp = False
        self.count = 0
        rowCount = 0
        for y in range(0, int(yDim/self.size), -1):
            row = []
            col = 0
            for x in range(int(xDim/self.size)):
                row.append(False)
                col += 1
            self.gridLocations.append(row)
            rowCount += 1

    def shouldAdd(self, startX, startY):
        self.isUp = False
        shouldAdd = False

        currX = startX
        currY = startY

        locationsToSetTrue = []
        x = int(currX/0.1)
        y = int(currY/0.1)
        allLocations = []
        numFilled = 0.0

        # Simplified for loop, doesn't seem to be working when I tested the squares
        # count = 0
        # for xD in range(-int(self.range/self.size), int(self.range/self.size)):
        #     for yD in range(-int(self.range/self.size), int(self.range/self.size)):
        #         # count += 1
        #         # print(count)
        #         if x+xD >= 0 and abs(y)+yD >=0 and x + xD < len(self.gridLocations[0]) and abs(y) + yD < len(self.gridLocations):
        #             allLocations.append([abs(y) + yD, x + xD])
        #             if self.gridLocations[abs(y) + yD][x + xD]:
        #                 numFilled += 1.0
        for xD in range(int(self.range/self.size)):
            for yD in range(int(self.range/self.size)):
                if x + xD < len(self.gridLocations[0]) and abs(y) + yD < len(self.gridLocations):
                    allLocations.append([abs(y) + yD, x + xD])
                    if self.gridLocations[abs(y) + yD][x + xD]:
                        numFilled += 1.0
                if yD != 0 and xD != 0 and x + xD < len(self.gridLocations[0]) and abs(y) - yD >= 0:
                    allLocations.append([abs(y) - yD, x + xD])
                    if self.gridLocations[abs(y) - yD][x + xD]:
                        numFilled += 1.0

                if yD != 0 and xD != 0 and x - xD >= 0 and abs(y) + yD < len(self.gridLocations):
                    allLocations.append([abs(y) + yD, x - xD])
                    if self.gridLocations[abs(y) + yD][x - xD]:
                        numFilled += 1.0

                if yD != 0 and xD != 0 and x - xD >= 0 and abs(y) - yD >= 0:
                    allLocations.append([abs(y) - yD, x - xD])
                    if self.gridLocations[abs(y) - yD][x - xD]:
                        numFilled += 1.0
            
            # percentage of nearby locations that are already filled
            numFilled /= (self.range/self.size) * (self.range/self.size) * 4

            # if none of the nearby locations are filled, paint this step
            if numFilled <= 0: 
                locationsToSetTrue.extend(allLocations)
                for location in locationsToSetTrue:
                    self.gridLocations[location[0]][location[1]] = True
                shouldAdd = True

            # Otherwise, go to beginning of this step and go up
            else:    
                shouldAdd = False

            return shouldAdd

    def getParsedCommands(self, startX, startY, endX, endY):
        self.isUp = False
        self.allLines.extend((startX, startY, endX, endY))
        self.count += 1
        commands = []
        numSteps = 0

        currX = startX
        currY = startY
        numSteps = int(math.sqrt((endX - startX)**2 + (endY - startY)**2)/0.1)
        step = 0

        locationsToSetTrue = []
        while step <= numSteps:
            x = int(currX/0.1)
            y = int(currY/0.1)
            allLocations = []
            numFilled = 0.0

            # Simplified for loop, doesn't seem to be working when I tested the squares
            # count = 0
            # for xD in range(-int(self.range/self.size), int(self.range/self.size)):
            #     for yD in range(-int(self.range/self.size), int(self.range/self.size)):
            #         # count += 1
            #         # print(count)
            #         if x+xD >= 0 and abs(y)+yD >=0 and x + xD < len(self.gridLocations[0]) and abs(y) + yD < len(self.gridLocations):
            #             allLocations.append([abs(y) + yD, x + xD])
            #             if self.gridLocations[abs(y) + yD][x + xD]:
            #                 numFilled += 1.0
            for xD in range(int(self.range/self.size)):
                for yD in range(int(self.range/self.size)):
                    if x + xD < len(self.gridLocations[0]) and abs(y) + yD < len(self.gridLocations):
                        allLocations.append([abs(y) + yD, x + xD])
                        if self.gridLocations[abs(y) + yD][x + xD]:
                            numFilled += 1.0
                    if yD != 0 and xD != 0 and x + xD < len(self.gridLocations[0]) and abs(y) - yD >= 0:
                        allLocations.append([abs(y) - yD, x + xD])
                        if self.gridLocations[abs(y) - yD][x + xD]:
                            numFilled += 1.0

                    if yD != 0 and xD != 0 and x - xD >= 0 and abs(y) + yD < len(self.gridLocations):
                        allLocations.append([abs(y) + yD, x - xD])
                        if self.gridLocations[abs(y) + yD][x - xD]:
                            numFilled += 1.0

                    if yD != 0 and xD != 0 and x - xD >= 0 and abs(y) - yD >= 0:
                        allLocations.append([abs(y) - yD, x - xD])
                        if self.gridLocations[abs(y) - yD][x - xD]:
                            numFilled += 1.0
            
            # percentage of nearby locations that are already filled
            numFilled /= (self.range/self.size) * (self.range/self.size) * 4

            # if none of the nearby locations are filled, paint this step
            if numFilled <= 0:  
                locationsToSetTrue.extend(allLocations)
                if self.isUp:
                    self.isUp = False
                    commands.append('DOWN')
                commands.append((currX, currY))

            # Otherwise, go to beginning of this step and go up
            else:    
                commands.append((currX, currY))
                if not self.isUp:
                    commands.append('UP')
                    self.isUp = True

            # find next x and y for beginning of next step based on vector math
            # formula provided by Dr. Bletsch
            percentDone = float(step+1)/float(numSteps)
            currX = (1-percentDone) * startX + percentDone * endX
            currY = (1-percentDone) * startY + percentDone * endY
            step += 1

        # Set locations to true that should be set to true AFTER for loop so that
        # lines don't get messed up along the way
        for location in locationsToSetTrue:
            self.gridLocations[location[0]][location[1]] = True
        
        newCommands = self.__parseCommands(startX, startY, commands)

        if (startX == 47 and startY == -17) and (endX == 46 and endY == -18):
            print(self.count)
            print(newCommands)
        if (startX == 46 and startY == -18) and (endX == 47 and endY == -19):
            print(self.count)
            print(newCommands)
        # return commands
        return newCommands


    def __parseCommands(self, startX, startY, commands):
        parsedCommands = []
        
        realStartX = startX
        realStartY = startY
        realEndX = startX
        realEndY = startY
        shouldCutOff = False
        nextCommandStart = False
        # Basically, we only want up to two x,y coordinates between any up/down command
        # since "DOWN", (1,0), (1, 0.1), (1, 0.2), "UP" is equivalent to "DOWN", (1,0), (1, 0.2), "UP"
        for command in commands:
            if command == 'UP' or command == 'DOWN':
                parsedCommands.append((realStartX, realStartY))
                parsedCommands.append((realEndX, realEndY))
                parsedCommands.append(command)
                shouldCutOff = True
                nextCommandStart = True
            elif nextCommandStart:
                shouldCutOff = False
                nextCommandStart = False
                realStartX = command[0]
                realStartY = command[1] 
            elif not shouldCutOff:
                realEndX = command[0]
                realEndY = command[1]

        parsedCommands.append((realStartX, realStartY))
        parsedCommands.append((realEndX, realEndY))

        # return parsedCommands
        realParsedCommands = []

        # Shouldn't have more than one x,y coordinate between an up command and a down command
        # since it only matters what the last x,y coordinate is
        # ex. "UP", (1, 1), (2,1), (3,1), "DOWN" is equivalent to "UP", (3,1), "DOWN"
        shouldAdd = True
        for index in range(len(parsedCommands)):
            if(parsedCommands[index] == 'UP'):
                shouldAdd = False
                realParsedCommands.append(parsedCommands[index])
                continue
            if index + 1 >= len(parsedCommands):
                shouldAdd = True
            elif(parsedCommands[index+1] == 'DOWN'):
                shouldAdd = True
            if(shouldAdd):
                realParsedCommands.append(parsedCommands[index])
        
        
        return realParsedCommands

