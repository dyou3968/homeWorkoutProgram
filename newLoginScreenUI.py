#############################################################################
"""
This is the new user login screen that the user sees before they place
their information into the database.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *

class NewLoginScreen(Mode):
    def appStarted(self):
        # Image Portion
        image = 'backAndNextButtons.jpg'
        # Image taken from https://stock.adobe.com/images/next-and-lbackr-web-buttons-internet-continue-click-here-go/29583568
        self.image = self.loadImage(image)
        self.nextButton = self.image.crop((60,60,440,160))
        self.resizer = 2/5
        self.nextButtonScaled = self.scaleImage(self.nextButton,self.resizer)
        self.backButton = self.image.crop((60,240,440,340))
        self.backButtonScaled = self.scaleImage(self.backButton,self.resizer)

#############################################################################
# Controller Portion
#############################################################################

    def mousePressed(self, event):
        (backX1,backX2,backY1,backY2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (nextX1,nextX2,nextY1,nextY2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,backX1,backX2,backY1,backY2):
            self.app.setActiveMode(self.app.StartScreen)
        if checkClickInBox.checkInBox(event.x, event.y,nextX1,nextX2,nextY1,nextY2):
            self.app.setActiveMode(self.app.NewUserInformationScreen)

#############################################################################
# View Portion
#############################################################################

    def createNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.nextButtonScaled))

    def createBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.backButtonScaled))

    def drawText(self,canvas):
        font = getFontSize.fontSize(42)
        message = "Before we get started, I need you to enter some information."
        canvas.create_text(self.width/2,self.height*2/5,text = "Welcome!",font = font)
        canvas.create_text(self.width/2,self.height*3/5,text = message,font = getFontSize.fontSize(32))

    def redrawAll(self,canvas):
        self.createNextBox(canvas)
        self.createBackBox(canvas)
        self.drawText(canvas)
