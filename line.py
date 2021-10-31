import math

class Line():
    beginX = 0.0
    beginY = 0.0
    endX = 0.0
    endY = 0.0

    orientation = ""

    def __init__(self, beginX, beginY, endX, endY):
        self.beginX = beginX
        self.beginY = beginY
        self.endX = endX
        self.endY = endY

        if(beginY == endY): self.orientation = "y"
        elif(beginX == endX): self.orientation = "x"
        else: self.orientation = "xy"
    
    def shouldDraw(self, line):
        if self.orientation != line.orientation:
            return True
        if self.orientation == "y":
            if abs(self.beginX - line.beginX) > 2:
                return True
            else:
                return False
        elif self.orientation == "x": 
            if abs(self.beginY - line.beginY) > 2:
                return True
            else:
                return False
        else: 
            if math.sqrt(abs(self.beginY - line.beginY)**2 + abs(self.beginX - line.beginX)) > 2:
                return True
            else:
                return False

    def getBeginX(self):
        return self.beginX

    def getBeginY(self):
        return self.beginY
    
    def getEndX(self):
        return self.endX
    
    def getEndY(self):
        return self.endY



    
