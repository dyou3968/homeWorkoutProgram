# cmu_112_graphics notes and documentation taken from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

from cmu_112_graphics import *

#########################################################
# Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#########################################################
class viewToModel(object):
    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by self.
        return ((self.margin <= x <= self.width-self.margin) and
                (self.margin <= y <= self.height-self.margin))

    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not viewToModel.pointInGrid(self,x, y)):
            return (-1, -1)
        gridWidth  = self.width - 2*self.margin
        gridHeight = self.height - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, self.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)
        return (row, col)

class modelToView(object):
    def getCellBounds(self, row, col):
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = self.width - 2*self.margin
        gridHeight = self.height - 2*self.margin
        columnWidth = gridWidth / self.cols
        rowHeight = gridHeight / self.rows
        x1 = self.margin + col * columnWidth
        x2 = self.margin + (col+1) * columnWidth
        y1 = self.margin + row * rowHeight
        y2 = self.margin + (row+1) * rowHeight
        return (x1, y1, x2, y2)

#########################################################
#########################################################

class checkClickInBox(object):
    def checkInBox(x,y,x1,x2,y1,y2):
        return ((x1 <= x <= x2) and (y1 <= y <= y2))

class generixBoxDimensions(object):
    def lowerRightBoxDimensions(self):
        x1 = (15/20)*self.width
        x2 = (19/20)*self.width
        y1 = (18/20)*self.height
        y2 = (19/20)*self.height
        return (x1,x2,y1,y2)

    def lowerLeftBoxDimensions(self):
        x1 = (1/20)*self.width
        x2 = (5/20)*self.width
        y1 = (18/20)*self.height
        y2 = (19/20)*self.height
        return (x1,x2,y1,y2)

class getFontSize(object):
    def fontSize(size):
        return f'Times_New_Roman {size} bold'