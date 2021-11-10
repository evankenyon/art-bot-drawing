import math

from grid_location import GridLocation


class Grid(object):

    def __init__(self, xDim, yDim):
        self.xDim = xDim
        self.yDim = yDim
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


    def getParsedCommands(self, startX, startY, endX, endY):
        self.count = 0
        commands = []
        xStep = 0
        yStep = 0
        numSteps = 0

        if startY < endY:
            yStep = self.size
        elif startY > endY:
            yStep = -self.size
        else:
            yStep = 0

        if startX < endX:
            xStep = self.size
        elif startX > endX:
            xStep = -self.size
            
        else:
            xStep = 0


        currX = startX
        currY = startY
        numSteps = int(math.sqrt((endX - startX)**2 + (endY - startY)**2)/0.1)
        step = 0
        # print(numSteps)
        # currStartX = currX
        # currStartY = currY
        # print(numSteps)
        locationsToSetTrue = []
        while step <= numSteps:
            # print(step)
            x = int(currX/0.1)
            y = int(currY/0.1)
            allLocations = []
            numFilled = 0.0
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
            
            numFilled /= (self.range/self.size) * (self.range/self.size) * 2
            # print(numFilled)
            # print(numFilled)

            if numFilled <= 0:  
                locationsToSetTrue.extend(allLocations)
                if self.isUp:
                    self.isUp = False
                    commands.append('DOWN')
                commands.append((currX, currY))
            else:    
                commands.append((currX, currY))
                if not self.isUp:
                    commands.append('UP')
                self.isUp = True
        
            percentDone = float(step+1)/float(numSteps)
            currX = (1-percentDone) * startX + percentDone * endX
            currY = (1-percentDone) * startY + percentDone * endY
            step += 1

        for location in locationsToSetTrue:
            self.gridLocations[location[0]][location[1]] = True
        
        # print(commands)

        parsedCommands = []
        
        realStartX = startX
        realStartY = startY
        realEndX = startX
        realEndY = startY
        shouldCutOff = False
        nextCommandStart = False
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

    def __getNearbyGridLocations(self, row, column, orientation):
        gridLocations = []
        if orientation == 'x':
            currRow = row
            while currRow < row + 20 and currRow > 0 and currRow < len(self.gridLocations):
                gridLocations.append(self.gridLocations[currRow][column])
                currRow += 1

            currRow = row - 1
            while currRow > row - 20 and currRow > 0 and currRow < len(self.gridLocations):
                gridLocations.append(self.gridLocations[currRow][column])
                currRow -= 1

        elif orientation == 'y':
            currCol = column
            # print(currCol)
            # print(column)
            # print(self.gridLocations[0])
            while currCol < column + 20 and currCol > 0 and currCol < len(self.gridLocations[0]):
                gridLocations.append(self.gridLocations[row][currCol])
                currCol += 1

            currCol = column - 1
            while currCol > column - 20 and currCol > 0 and currCol < len(self.gridLocations[0]):
                gridLocations.append(self.gridLocations[row][currCol])
                currCol -= 1

        elif orientation == 'xy':
            currCol = column
            currRow = row
            while currCol < column + 20 and currRow > 0 and currRow < len(self.gridLocations) and currCol > 0 and currCol < len(self.gridLocations[0]):
                gridLocations.append(self.gridLocations[row][currCol])
                currCol += 1
                currRow += 1

            currCol = column - 1
            currRow = row - 1
            while currCol > row - 20 and currRow > 0 and currRow < len(self.gridLocations) and currCol > 0 and currCol < len(self.gridLocations[0]):
                gridLocations.append(self.gridLocations[row][currCol])
                currCol -= 1
                currRow -= 1
        
        return gridLocations
        



    def __findGridLocation(self, x, y):
        # Right now the gcode is all integers, might have to change if we go the 
        # scale down route (i.e. scale up picture for detail when creating initial commands, then scale 
        # down for usage on CNC)

        # print("is this even being called?")
        # print(str(x) + ", " + str(y))
        for gridLocationRow in self.gridLocations:
            # print(gridLocationRow)
            for gridLocation in gridLocationRow:
                # print(str(gridLocation.getXPos()) + ", " + str(gridLocation.getYPos()))
                if gridLocation.getXPos() == x and gridLocation.getYPos() == y:
                    return gridLocation
