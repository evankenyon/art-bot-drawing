from grid_location import GridLocation


class Grid(object):

    def __init__(self, xDim, yDim):
        self.xDim = xDim
        self.yDim = yDim
        self.gridLocations = []
        self.size = 0.1
        self.isUp = False
        self.count = 0
        rowCount = 0
        for y in range(0, int(yDim/self.size), -1):
            row = []
            col = 0
            # print("test1")
            for x in range(int(xDim/self.size)):
                # print("test2")
                row.append(GridLocation(round(x * self.size, 1), round(y * self.size, 1), rowCount, col, round(x * self.size, 1), round(y * self.size, 1)))
                col += 1
            # print(row)
            self.gridLocations.append(row)
            rowCount += 1


    def getParsedCommands(self, startX, startY, endX, endY):
        print(self.count)
        self.count += 1
        commands = []
        xStep = 0
        yStep = 0
        numSteps = 0

        if startY < endY:
            yStep = self.size
            numSteps = round((endY-startY)/yStep, 0)
        elif startY > endY:
            yStep = -self.size
            numSteps = round((endY-startY)/yStep, 0)
        else:
            yStep = 0

        if startX < endX:
            xStep = self.size
            numSteps = round((endX-startX)/xStep, 0)
        elif startX > endX:
            xStep = -self.size
            numSteps = round((endX-startX)/xStep, 0)
        else:
            xStep = 0

        currX = round(startX, 1)
        currY = round(startY, 1)

        orientation = ""
        if xStep != 0 and yStep !=0:
            orientation = 'xy'
        elif xStep != 0:
            orientation = 'x'
        elif yStep != 0:
            orientation = 'y'

        
        step = 0

        while step < numSteps:
            gridLocation = self.__findGridLocation(currX, currY)
            nearbyGridLocations = self.__getNearbyGridLocations(gridLocation.getRow(), gridLocation.getCol(), orientation)
            filledUp = 0.0

            for location in nearbyGridLocations:
                if location.getIsFilledIn():
                    filledUp += 1.0
            
            filledUp /= len(nearbyGridLocations)
            # print(filledUp)
            
            if filledUp > 0.25:
                commands.append((currX, currY))
                if not self.isUp:
                    commands.append('UP')
                self.isUp = True
            else:
                if self.isUp:
                    self.isUp = False
                    commands.append('DOWN')
                for location in nearbyGridLocations:
                    location.setIsFilledInTrue()
                # gridLocation.setIsFilledInTrue()
                commands.append((currX, currY))
            
            currX = round(currX + xStep, 1)
            currY = round(currY + yStep, 1)
            step += 1


                
            # if not gridLocation.getIsFilledIn():
            #     if self.isUp:
            #         self.isUp = False
            #         commands.append('DOWN')
            #     gridLocation.setIsFilledInTrue()
            #     commands.append((currX, currY))
            # else:
            #     commands.append((currX, currY))
            #     if not self.isUp:
            #         commands.append('UP')
            #     self.isUp = True

            # currX += xStep
            # currY += yStep
        
        # lines = []

        # for i in range(-20, 21):
        #     if i == 0:
        #         continue
        #     newStartY = startY + i * self.size
        #     newEndY = endY + i * self.size
        #     for gridLocation 

        return commands

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
