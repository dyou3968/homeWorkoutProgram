#############################################################################
"""
This is the new user login screen that the user sees before they place
their information into the database.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *

class NewLoginScreen(Mode):

    def mousePressed(self, event):
        (backX1,backX2,backY1,backY2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (nextX1,nextX2,nextY1,nextY2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,backX1,backX2,backY1,backY2):
            self.app.setActiveMode(self.app.StartScreen)
        if checkClickInBox.checkInBox(event.x, event.y,nextX1,nextX2,nextY1,nextY2):
            self.app.setActiveMode(self.app.NewUserInformationScreen)

    def drawInputBoxes(self,text,font,x1,x2,y1,y2,canvas):
            canvas.create_text((x1+x2)/2,(y1+y2)/2,text = text, font = font)

    def createNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        self.drawInputBoxes("Next","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def createBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        self.drawInputBoxes("Back","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def drawText(self,canvas):
        font = getFontSize.fontSize(42)
        message = "Before we get started, I need you to enter some information."
        canvas.create_text(self.width/2,self.height*2/5,text = "Welcome!",font = font)
        canvas.create_text(self.width/2,self.height*3/5,text = message,font = getFontSize.fontSize(32))

    def redrawAll(self,canvas):
        self.createNextBox(canvas)
        self.createBackBox(canvas)
        self.drawText(canvas)
