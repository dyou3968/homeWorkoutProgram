#############################################################################
"""
This is the main screen where the user chooses the specific body part they 
want to workout, and how much time they have.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *
from exerciseGenerator import *

class MainScreen(Mode):
    def appStarted(self):
        self.intensity = "Input Intensity Here"
        self.bodyPart = "Input Category Here"
        [self.username, self.password, self.gender, 
            self.weight, self.age, self.activityLevel] = getCurrentUser()
        self.workoutList = "test"
        self.showExercises = False

    def mousePressed(self, event):
        (bottomX1,bottomX2,bottomY1,bottomY2) = generixBoxDimensions.lowerBoxDimensions(self)
        (intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2) = (0,(1/4)*self.width,(6/8)*self.height,(7/8)*self.height)
        (categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2) = ((1/4)*self.width,(1/2)*self.width,(6/8)*self.height,(7/8)*self.height)
        if checkClickInBox.checkInBox(event.x,event.y,bottomX1,bottomX2,bottomY1,bottomY2):
            if self.verifyInputs():
                self.workoutList = workoutGenerator(getCurrentUser(),self.bodyPart,self.intensity)
                self.getWorkoutText()
                self.getWorkoutDescriptionText()
                self.showExercises = True
        elif checkClickInBox.checkInBox(event.x,event.y,intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2):
            self.getIntensity(event)
        elif checkClickInBox.checkInBox(event.x,event.y,categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2):
            self.getBodyPart(event)

    def verifyInputs(self):
        if ((self.bodyPart in ["legs","core","back","chest","full","plyos"]) and 
            ((self.intensity >= 1) and (self.intensity <= 5))):
            return True

    def userStatsPart1(self):
        self.userInfoPart1 = f'Gender: {self.gender} \n Weight: {self.weight}'
        return self.userInfoPart1

    def userStatsPart2(self):
        self.userInfoPart2 = f' Age: {self.age} \n Activity Level: {self.activityLevel}'
        return self.userInfoPart2

    def getWorkoutText(self):
        text = 'Exercise Generated:'
        for entry in self.workoutList:
            exercise = entry[0]
            text += "\n" + exercise
        return text

    def getWorkoutDescriptionText(self):
        text = 'Exercise Descriptions:'
        for entry in self.workoutList:
            exercise = entry[1]
            text += "\n" + exercise
        return text

#############################################################################
# User inputs:
#   body part they want to work on
#   intensity of the workout
#   amount of time they have to workout

# Additional Inputs to add:
#   User goal: I.e: Gain muscle or lose weight
#############################################################################

    def getIntensity(self, event):
        self.intensity = self.getUserInput('Enter your intensity level from 1 to 5 \n with 5 being the highest')
        try:
            self.intensity = int(self.intensity)
            if (self.intensity == None):
                self.intensity = "Must enter intensity to continue"
            elif (self.intensity < 1) or (self.intensity > 5):
                self.intensity = "Must be number \n between \n 1 and 5 inclusive"
            else:
                self.intensity = self.intensity
        except: 
            self.intensity = "Must be whole number"

    def getBodyPart(self, event):
        self.bodyPart = self.getUserInput('Enter your category here \n Categories: legs, core, back, chest, full, and plyos')
        if (self.bodyPart == None):
            self.bodyPart = "Must enter category \n to continue"
        elif (self.bodyPart not in ["legs","core","back","chest","full","plyos"]):
            self.bodyPart = "Must be written \n exactly to continue"
        else:
            self.bodyPart = self.bodyPart

#############################################################################
# View Portion
#############################################################################

    def drawBottomBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "medium sea green")
        inputBoxes.drawInputBoxes(self,"Generate Workout",getFontSize.fontSize(40),x1,x2,y1,y2,canvas)

    def drawIntensityBox(self,canvas):
        (x1,x2,y1,y2) = (0,(1/4)*self.width,(6/8)*self.height,(7/8)*self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "orange2")
        inputBoxes.drawInputBoxes(self,f'Intensity: \n {self.intensity}',getFontSize.fontSize(20),x1,x2,y1,y2,canvas)

    def drawCategoryBox(self,canvas):
        (x1,x2,y1,y2) = ((1/4)*self.width,(1/2)*self.width,(6/8)*self.height,(7/8)*self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "orange2")
        inputBoxes.drawInputBoxes(self,f'Category: \n {self.bodyPart}',getFontSize.fontSize(20),x1,x2,y1,y2,canvas)

    def drawUserProfileBoxPart1(self,canvas):
        (x1,x2,y1,y2) = ((1/2)*self.width,(3/4)*self.width,(6/8)*self.height,(7/8)*self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "orange2")
        inputBoxes.drawInputBoxes(self,self.userStatsPart1(),getFontSize.fontSize(26),x1,x2,y1,y2,canvas)

    def drawUserProfileBoxPart2(self,canvas):
        (x1,x2,y1,y2) = ((3/4)*self.width,self.width,(6/8)*self.height,(7/8)*self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "orange2")
        inputBoxes.drawInputBoxes(self,self.userStatsPart2(),getFontSize.fontSize(26),x1,x2,y1,y2,canvas)

    def drawWorkoutText(self,canvas):
        canvas.create_text(self.width/2,self.height/4, text = self.getWorkoutText(), font = getFontSize.fontSize(36))

    def redrawAll(self, canvas):
        self.drawBottomBox(canvas)
        self.drawIntensityBox(canvas)
        self.drawCategoryBox(canvas)
        self.drawUserProfileBoxPart1(canvas)
        self.drawUserProfileBoxPart2(canvas)
        if self.showExercises:
            self.drawWorkoutText(canvas)


