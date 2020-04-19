from cmu_112_graphics import *
from helperFunctionsUI import *

class ReturnLoginScreen(Mode):
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

    def mousePressed(self, event):
        (row, col) = viewToModel.getCell(self,event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.selection == (row, col)):
            self.selection = (-1, -1)
        else:
            self.selection = (row, col)

#########################################################

        if self.selection == (0,1) :
            self.getUsername(event)
        elif self.selection == (1,1):
             self.getPassword(event)

        (backX1,backX2,backY1,backY2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (nextX1,nextX2,nextY1,nextY2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,backX1,backX2,backY1,backY2):
            self.app.setActiveMode(self.app.StartScreen)
        # if checkClickInBox.checkInBox(event.x, event.y,nextX1,nextX2,nextY1,nextY2):
        #     self.app.setActiveMode(self.app.ReturnLoginScreen)

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

    def createTextInBoxes(self,row,col,font,x1,x2,y1,y2,canvas):
            if (row == 0) and (col == 0):
                self.drawInputBoxes("Username",font,x1,x2,y1,y2,canvas)
            if (row == 1) and (col == 0):
                self.drawInputBoxes("Password",font,x1,x2,y1,y2,canvas)
            # User Input column
            if (row == 0) and (col == 1):
                self.drawInputBoxes(self.username,font,x1,x2,y1,y2,canvas)
            if (row == 1) and (col == 1):
                self.drawInputBoxes(self.password,font,x1,x2,y1,y2,canvas)

    def createTextBoxes(self,canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = modelToView.getCellBounds(self,row,col)
                font = "Times_New_Roman 36 bold"
                self.createTextInBoxes(row,col,font,x1,x2,y1,y2,canvas)
                canvas.create_rectangle(x1,y1,x2,y2, outline = "black")

    def createNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        self.drawInputBoxes("Next","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def createBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        self.drawInputBoxes("Back","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def redrawAll(self,canvas):
        self.createTextBoxes(canvas)
        self.createNextBox(canvas)
        self.createBackBox(canvas)