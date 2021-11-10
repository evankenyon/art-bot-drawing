class GridLocation(object):

    def __init__(self, xPos, yPos, row, col, length, height):
        self.xPos = xPos
        self.yPos = yPos
        self.length = length
        self.height = height
        self.isFilledIn = False
        self.row = row
        self.col = col
    
    def doesOverlap(self, startX, startY, endX, endY):
        # if startX != endX and startY != endY:
        #     # diagonal

        # elif startX != endX:
        #     # only x changing
        # else:
        #     # only y changing

        # Currently only checking if overlaps entire GridLocation, should be fine
        # since planning on making them pretty small, but check this if errors occur
        doesXOverlap = startX < self.xPos and endX >= self.xPos + self.length
        doesYOverlap = startY < self.yPos and endY >= self.yPos + self.height
        return doesXOverlap and doesYOverlap

    def getIsFilledIn(self):
        return self.isFilledIn
    
    def setIsFilledInTrue(self):
        self.isFilledIn = True
    
    def getXPos(self):
        return self.xPos

    def getYPos(self):
        return self.yPos

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col
    

    
        
