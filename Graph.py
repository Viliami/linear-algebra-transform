from screen import *
import numpy as np

class Graph2D(Surface):
    def __init__(self, width, height, xAxis, yAxis):
        super().__init__(width, height)
        self.xAxis, self.yAxis = xAxis, yAxis
        self.showGrid = True
        self.points = []
        coord = []
        for x in self.xAxis:
            for y in self.yAxis:
                coord.append(np.array([x,y]))
        self.grid = np.array(coord)
        self.normalGridColor = (200,200,200)
        self.animationFrame = 0
        self.transformMatrix = 0
        self.originalGrid = self.grid
        self.animationLength = 0
        self.temp = np.identity(2)

    def toPixel(self, cX, cY): #coordinates to pixels
        cX -= self.xAxis[0]
        cY = (self.yAxis[-1]) - cY
        xRatio = self.width/len(self.xAxis)
        yRatio = self.height/len(self.yAxis)
        return (int(cX*xRatio), int(cY*yRatio))

    def renderGrid(self):
        xPoints, yPoints = len(self.xAxis), len(self.yAxis)
        for i in range(-xPoints, xPoints):
            self.line(self.toPixel(i,-yPoints), self.toPixel(i,yPoints),self.normalGridColor)
        for i in range(-yPoints, yPoints):
            self.line(self.toPixel(-xPoints,i), self.toPixel(xPoints,i),self.normalGridColor)            

        for i in range(0,len(self.grid),xPoints):
            self.line(self.toPixel(*self.grid[i]),self.toPixel(*self.grid[i+(xPoints-1)]))
            self.line(self.toPixel(*self.grid[i//xPoints]),self.toPixel(*self.grid[len(self.grid)-xPoints+i//xPoints]))

    def render(self):
        self.fill(self.backgroundColor)
        if(self.showGrid):
            self.renderGrid()
        for point in self.points:
            self.renderPoint(point)
        if(self.animationFrame):
            self.transform(self.transformMatrix)

    def renderLine(self, point, point2):
        self.line(self.toPixel(*(self.temp @ point[0])), self.toPixel(*(self.temp @ point2[0])), BLACK, 2)

    def renderPoint(self, point):
        self.filledCircle(self.toPixel(*(self.temp @ point[0])), point[2], point[1], (0,0,0))

    def plot(self, x, y, color, radius):
        self.points.append(((x,y),color,radius))

    def transform(self, matrix, animationLength=None):
        self.animationFrame-=1
        if(animationLength):
            self.animationFrame = animationLength
            self.animationLength = animationLength
        identity = np.identity(2)
        if(type(self.transformMatrix) is not np.ndarray):
            self.originalGrid = self.grid
            self.transformMatrix = matrix

        self.temp = matrix - ((matrix-identity)*(self.animationFrame/self.animationLength))
        self.grid = (self.temp @ self.originalGrid.T).T
