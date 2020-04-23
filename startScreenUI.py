#############################################################################
"""
This is the new start screen information that the user first sees when they run
the program. 
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *

class StartScreen(Mode):
    # Program start screen
    def appStarted(self):
        self.newUser = "New User"
        self.returningUser = "Returning User"
        self.message = "Home Fitness Workout Program"

    def mousePressed(self, event):
        (returnUserx1,returnUserx2,returnUsery1,returnUsery2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (newUserx1,newUserx2,newUsery1,newUsery2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,newUserx1,newUserx2,newUsery1,newUsery2):
            self.app.setActiveMode(self.app.NewLoginScreen)
        if checkClickInBox.checkInBox(event.x, event.y,returnUserx1,returnUserx2,returnUsery1,returnUsery2):
            self.app.setActiveMode(self.app.ReturnLoginScreen)

    def createNewUserBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        inputBoxes.drawInputBoxes(self,"New User","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def createReturningUserBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        inputBoxes.drawInputBoxes(self,"Returning User","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def createUserBoxes(self,canvas):
        self.createNewUserBox(canvas)
        self.createReturningUserBox(canvas)

    def redrawAll(self,canvas):
        font = 'Times_New_Roman 42 bold'
        canvas.create_text(self.width/2,self.height*2/5,text = self.message,font = font)
        self.createUserBoxes(canvas)
