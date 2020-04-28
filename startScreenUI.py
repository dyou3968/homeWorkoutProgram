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
        self.message = "Home Fitness Workout Program"

        # Taken from https://www.shutterstock.com/search/running%2Bsprite?section=1&image_type=vector&safe=true&search_source=base_related_searches&saveFiltersLink=true
        self.image = "runningAnimation.png"
        self.spriteStripLeft = self.loadImage(self.image)
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
        self.leftY = random.randrange(20,self.height*3//4)
        self.rightY = random.randrange(20,self.height*3//4)
        self.timerDelay = 100

    def getTimerDelay(self):
        return self.timerDelay

    def timerFired(self):
        self.spriteCounterLeft = (5 + self.spriteCounterLeft) % len(self.spritesLeft)
        self.spriteCounterRight = (5 + self.spriteCounterRight) % len(self.spritesRight)
        self.leftX = (self.leftX - 30) % self.width
        self.rightX = (self.rightX + 15) % self.width
        if self.leftX <= 10:
            self.leftY = random.randrange(20,self.height*3//4)
        if self.rightX >= self.width-10:
            self.rightY = random.randrange(20,self.height*3//4)


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

    def drawTitle(self,canvas):
        font = 'Times_New_Roman 42 bold'
        canvas.create_text(self.width/2,self.height*2/5,text = self.message,font = font)

    def drawSpriteLeft(self,canvas):
        sprite = self.spritesLeft[self.spriteCounterLeft]
        canvas.create_image(self.leftX, self.leftY, image=ImageTk.PhotoImage(sprite))

    def drawSpriteRight(self,canvas):
        sprite = self.spritesRight[self.spriteCounterRight]
        canvas.create_image(self.rightX, self.rightY, image=ImageTk.PhotoImage(sprite))

    def drawSprites(self,canvas):
        self.drawSpriteLeft(canvas)
        self.drawSpriteRight(canvas)

    def redrawAll(self,canvas):
        self.drawSprites(canvas)
        self.drawTitle(canvas)
        self.createUserBoxes(canvas)

# class MyApp(ModalApp):
#     def appStarted(self):
#         self.StartScreen = StartScreen()
#         self.setActiveMode(self.StartScreen)
#         self.timerDelay = 100
    

# app = MyApp(width=1000, height=800)
