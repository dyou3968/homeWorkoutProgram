#############################################################################
"""
This is the new start screen information that the user first sees when they run
the program. 
"""

# Animation and other UI design taken from
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingApp
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *
import random

class StartScreen(Mode):
    # Program start screen
    def appStarted(self):
        self.newUser = "New User"
        self.returningUser = "Returning User"
        self.message = "Stay Fit"
        self.description = '''A home workout program designed \n to help you stay fit during quaratine'''
        self.creator = 'By David You'

############################################################
# Running Animation
############################################################
        # Taken from https://www.shutterstock.com/search/running%2Bsprite?section=1&image_type=vector&safe=true&search_source=base_related_searches&saveFiltersLink=true
        self.runningImage = "runningAnimation.png"
        self.spriteStripLeft = self.loadImage(self.runningImage)
        self.spriteStripRight = self.spriteStripLeft.transpose(Image.FLIP_LEFT_RIGHT)
        self.spritesLeft = []
        self.spritesRight = []
        for row in range(17):
            spriteLeft = self.spriteStripLeft.crop((532/17*row,0,532/17*(row+1),45))
            spriteRight = self.spriteStripRight.crop((532/17*row,0,532/17*(row+1),45))
            self.spritesLeft.append(spriteLeft)
            self.spritesRight.append(spriteRight)
        self.spriteCounterLeft = 0
        self.spriteCounterRight = 0
        self.leftX = self.width
        self.rightX = 0
        self.runningBounds = (self.height//3,self.height*3//4)
        self.leftY = random.randrange(self.runningBounds[0],self.runningBounds[1])
        self.rightY = random.randrange(self.runningBounds[0],self.runningBounds[1])

############################################################
# Logo
############################################################
        # Taken from https://www.shutterstock.com/search/barbell+logo
        barbellImage = 'barbellLogo.webp'
        self.image = self.loadImage(barbellImage)
        self.barbell = self.image.crop((40,90,220,170))
        self.resizer = 4
        self.barbellScaled = self.scaleImage(self.barbell,self.resizer)


#############################################################################
# Controller Portion
#############################################################################

    def timerFired(self):
        # Creates the animation of the left and right runners
        self.spriteCounterLeft = (10 + self.spriteCounterLeft) % len(self.spritesLeft)
        self.spriteCounterRight = (5 + self.spriteCounterRight) % len(self.spritesRight)
        self.leftX = (self.leftX - 30) % self.width
        self.rightX = (self.rightX + 15) % self.width
        if self.leftX <= 10:
            self.leftY = random.randrange(self.runningBounds[0],self.runningBounds[1])
        if self.rightX >= self.width-10:
            self.rightY = random.randrange(self.runningBounds[0],self.runningBounds[1])

    def mousePressed(self, event):
        (returnUserx1,returnUserx2,returnUsery1,returnUsery2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (newUserx1,newUserx2,newUsery1,newUsery2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,newUserx1,newUserx2,newUsery1,newUsery2):
            self.app.setActiveMode(self.app.NewLoginScreen)
        if checkClickInBox.checkInBox(event.x, event.y,returnUserx1,returnUserx2,returnUsery1,returnUsery2):
            self.app.setActiveMode(self.app.ReturnLoginScreen)


#############################################################################
# View Portion
#############################################################################

    def drawNewUserBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black", fill = "light goldenrod")
        inputBoxes.drawInputBoxes(self,"New User",getFontSize.fontSize(18),x1,x2,y1,y2,canvas)

    def drawReturningUserBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black", fill = "dodger blue")
        inputBoxes.drawInputBoxes(self,"Returning User",getFontSize.fontSize(18),x1,x2,y1,y2,canvas)

    def drawUserBoxes(self,canvas):
        self.drawNewUserBox(canvas)
        self.drawReturningUserBox(canvas)

    def drawTitle(self,canvas):
        cx,cy = self.width/2,self.height*1/6 - 20
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.barbellScaled))
        canvas.create_text(self.width/2,self.height*1/6,text = self.message,font = "Times_New_Roman 90 bold italic", fill = "blue4")

    def drawDescription(self,canvas):
        canvas.create_text(self.width/2,self.height*5/6-50,text = self.description,font = getFontSize.fontSize(30), fill = "black")
        canvas.create_text(self.width/2,self.height*7/8,text = self.creator,font = getFontSize.fontSize(40), fill = "black")

    def drawRunningSpriteLeft(self,canvas):
        sprite = self.spritesLeft[self.spriteCounterLeft]
        canvas.create_image(self.leftX, self.leftY, image=ImageTk.PhotoImage(sprite))

    def drawRunningSpriteRight(self,canvas):
        sprite = self.spritesRight[self.spriteCounterRight]
        canvas.create_image(self.rightX, self.rightY, image=ImageTk.PhotoImage(sprite))

    def drawSprites(self,canvas):
        self.drawRunningSpriteLeft(canvas)
        self.drawRunningSpriteRight(canvas)

    def redrawAll(self,canvas):
        self.drawTitle(canvas)
        self.drawUserBoxes(canvas)
        self.drawSprites(canvas)
        self.drawDescription(canvas)
