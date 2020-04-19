
# cmu_112_graphics notes and documentation taken from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

from cmu_112_graphics import *

class StartScreen(Mode):
    def appStarted(self):
        self.message = "Home Fitness Workout Program"

    def mousePressed(self, event):
        self.app.setActiveMode(self.app.LoginScreen)

    def redrawAll(self,canvas):
        self.x1 = self.width/4
        self.x2 = self.width*3/4
        self.y1 = self.height*2/3
        self.y2 = self.height*5/6

        self.textX = (self.x1 + self.x2)/2
        self.textY = (self.y1 + self.y2)/2
        font = 'Times_New_Roman 42 bold'
        canvas.create_text(self.width/2,self.height*2/5,text = self.message,
        font = font)
        canvas.create_text(self.textX,self.textY,text = 'Click Anywhere to Start', font = font)


class LoginScreen(Mode):
    def appStarted(self):
        self.rows = 2
        self.cols = 2
        self.margin = self.width/8
        self.selection = (-1.-1)
        self.username = "Click here"
        self.password = "Click here"

#########################################################
# From https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#########################################################

    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by self.
        return ((self.margin <= x <= self.width-self.margin) and
                (self.margin <= y <= self.height-self.margin))

    def getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y)):
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

    def mousePressed(self, event):
        (row, col) = self.getCell(event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.selection == (row, col)):
            self.selection = (-1, -1)
        else:
            self.selection = (row, col)

        if self.selection == (0,1) :
            self.getUsername(event)
        elif self.selection == (1,1):
             self.getPassword(event)


#########################################################

    def getUsername(self, event):
        username = self.getUserInput('Enter your username')
        if (username == None):
            self.username = "Must enter username to login"
        else:
            self.username = username

    def getPassword(self, event):
        password = self.getUserInput('Enter your password')
        if (password == None):
            self.password = "Must enter password to login"
        else:
            self.password = password

    def drawInputBoxes(self,text,font,x1,x2,y1,y2,canvas):
        canvas.create_text((x1+x2)/2,(y1+y2)/2,text = text, font = font)

    def __repr__(self):
        return f'{self.message}'

    def createTextBoxes(self,canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = self.getCellBounds(row,col)
                font = "Times_New_Roman 42 bold"
                if (row == 0) and (col == 0):
                    self.drawInputBoxes("Username",font,x1,x2,y1,y2,canvas)
                if (row == 1) and (col == 0):
                    self.drawInputBoxes("Password",font,x1,x2,y1,y2,canvas)
                canvas.create_rectangle(x1,y1,x2,y2, outline = "black")

                if (row == 0) and (col == 1):
                    self.drawInputBoxes(self.username,font,x1,x2,y1,y2,canvas)
                if (row == 1) and (col == 1):
                    self.drawInputBoxes(self.password,font,x1,x2,y1,y2,canvas)
                print(self.username,self.password)

    def redrawAll(self,canvas):
        self.createTextBoxes(canvas)

class MyApp(ModalApp):
    def appStarted(self):
        self.StartScreen = StartScreen()
        self.LoginScreen = LoginScreen()
        self.setActiveMode(self.StartScreen)

app = MyApp(width=1000, height=800)