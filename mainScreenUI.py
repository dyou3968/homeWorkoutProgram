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
        self.curWorkoutDescription = []
        self.heightAdjuster = 40
        self.time = -1

        # Boolean Conditions
        self.showExercises = False
        self.showWorkoutDescription = False
        self.showWorkoutDurationIncorrect = False

    def mouseMoved(self, event):
        if self.showExercises:
            start = 1
            for i in range(len(self.workoutList)):
                exercise = self.workoutList[i][0]
                (x1,x2,y1,y2) = ((1/4)*self.width,(3/4)*self.width,(start/16)*self.height,((start+1)/16)*self.height)
                if self.checkMoveBox(event.x,event.y,x1,x2,y1,y2):
                    self.showWorkoutDescription = True
                    self.workoutDescription = self.getWorkoutDescriptionList(self.workoutList[i][1])
                start += 1
            (headerX1,headerX2,headerY1,headerY2) = ((1/4)*self.width,(3/4)*self.width,(1/16)*self.height-self.heightAdjuster,(2/16)*self.height-self.heightAdjuster)
            if self.checkMoveBox(event.x,event.y,headerX1,headerX2,headerY1,headerY2):
                self.curWorkoutDescription = ""
                self.showWorkoutDescription = False
                
    def getWorkoutDescriptionList(self,text):
        self.curWorkoutDescription = (text.split("."))
        return self.curWorkoutDescription 
    
    def checkMoveBox(self,x,y,x1,x2,y1,y2):
        return ((x1 <= x <= x2) and (y1 <= y <= y2))

    def mousePressed(self, event):
        (bottomX1,bottomX2,bottomY1,bottomY2) = generixBoxDimensions.lowerBoxDimensions(self)
        (intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2) = (0,(1/4)*self.width,(6/8)*self.height,(7/8)*self.height)
        (categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2) = ((1/4)*self.width,(1/2)*self.width,(6/8)*self.height,(7/8)*self.height)
        if checkClickInBox.checkInBox(event.x,event.y,bottomX1,bottomX2,bottomY1,bottomY2):
            self.getTime(event)
            if (isinstance(self.time,int)) and (self.time >= 15):
                self.showWorkoutDurationIncorrect = False
                if self.verifyInputs():
                    self.workoutList, self.totalCalories = workoutGenerator(getCurrentUser(),self.bodyPart,self.intensity,self.time)
                    self.showExercises = True
            else:
                self.showWorkoutDurationIncorrect = True

        elif checkClickInBox.checkInBox(event.x,event.y,intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2):
            self.getIntensity(event)
        elif checkClickInBox.checkInBox(event.x,event.y,categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2):
            self.getBodyPart(event)

    def verifyInputs(self):
        if ((self.bodyPart in ["legs","core","back","chest","full","plyos"]) and 
            ((self.intensity >= 1) and (self.intensity <= 5)) and self.time >= 15):
            return True

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

    def getTime(self, event):
        self.time = self.getUserInput('How many minutes do you plan on exercising?')
        try:
            self.time = int(self.time)
            if (self.time == None):
                self.time = "Must enter time to continue"
            elif (self.time < 15):
                self.time = "Minimum workout time is 15 minutes"
            else:
                self.time = self.time
        except: 
            self.time = "Duration must be whole number"

    def getBodyPart(self, event):
        self.bodyPart = self.getUserInput('Enter your category here \n Categories: legs, core, back, chest, full, and plyos')
        if (self.bodyPart == None):
            self.bodyPart = "Must enter category \n to continue"
        elif (self.bodyPart not in ["legs","core","back","chest","full","plyos"]):
            self.bodyPart = "Must be written \n exactly to continue"
        else:
            self.bodyPart = self.bodyPart

    def userStatsPart1(self):
        self.userInfoPart1 = f'Gender: {self.gender} \n Weight: {self.weight}'
        return self.userInfoPart1

    def userStatsPart2(self):
        self.userInfoPart2 = f' Age: {self.age} \n Activity Level: {self.activityLevel}'
        return self.userInfoPart2

#############################################################################
# View Portion
#############################################################################

    def drawBottomBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "medium sea green")
        if self.showExercises:
            inputBoxes.drawInputBoxes(self,f'Workout Duration: {self.time} Minutes',getFontSize.fontSize(40),x1,x2,y1,y2,canvas)
        else:
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

    def drawHeader(self,canvas):
        (x1,x2,y1,y2) = ((1/4)*self.width,(3/4)*self.width,(1/16)*self.height-self.heightAdjuster,(2/16)*self.height-self.heightAdjuster)
        inputBoxes.drawInputBoxes(self,f"Estimated Calories Burned: {self.totalCalories}",getFontSize.fontSize(30),x1,x2,y1,y2,canvas)

    def drawWorkoutText(self,canvas):
        start = 2
        for i in range(len(self.workoutList)):
            exercise = self.workoutList[i][0]
            (x1,x2,y1,y2) = ((1/3)*self.width,(2/3)*self.width,(start/16)*self.height - self.heightAdjuster,((start+1)/16)*self.height - self.heightAdjuster)
            canvas.create_rectangle(x1,y1,x2,y2, outline = "white", fill = "white")
            inputBoxes.drawInputBoxes(self,exercise,getFontSize.fontSize(24),x1,x2,y1,y2,canvas)
            start += 1

    def drawWorkoutDescription(self,canvas):
        start = 13
        for i in range(len(self.curWorkoutDescription)):
            line = self.curWorkoutDescription[i]
            (x1,x2,y1,y2) = (0,self.width,(start/24)*self.height,((start+1)/24)*self.height)
            canvas.create_rectangle(x1,y1,x2,y2, outline = "white", fill = "white")
            inputBoxes.drawInputBoxes(self,line,getFontSize.fontSize(14),x1,x2,y1,y2,canvas)
            start += 1

    def drawWorkoutDurationIncorrect(self,canvas):
        canvas.create_text(self.width/2,self.height/2,text = f'{self.time}', fill = "red", font = getFontSize.fontSize(40))


    def redrawAll(self, canvas):
        self.drawBottomBox(canvas)
        self.drawIntensityBox(canvas)
        self.drawCategoryBox(canvas)
        self.drawUserProfileBoxPart1(canvas)
        self.drawUserProfileBoxPart2(canvas)
        if self.showExercises:
            self.drawWorkoutText(canvas)
            self.drawHeader(canvas)
        if self.showWorkoutDescription:
            self.drawWorkoutDescription(canvas)
        if self.showWorkoutDurationIncorrect:
            self.drawWorkoutDurationIncorrect(canvas)
