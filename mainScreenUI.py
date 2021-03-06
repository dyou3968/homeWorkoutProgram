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
        self.heightAdjuster = 40
        self.workoutMultiplier = 1

        # Boolean Conditions
        self.showExercises = False
        self.showWorkoutDescription = False
        self.showWorkoutDurationIncorrect = False
        self.showWorkoutInputsIncomplete = False
        self.timerPaused = False
        self.showWorkoutDuration = False

        # Image Portion
        image = 'backAndNextButtons.jpg'
        # Image taken from https://stock.adobe.com/images/next-and-lbackr-web-buttons-internet-continue-click-here-go/29583568
        self.image = self.loadImage(image)
        self.resizer = 2/5
        self.backButton = self.image.crop((60,240,440,340))
        self.backButtonScaled = self.scaleImage(self.backButton,self.resizer)


#############################################################################
# Controller Portion
#############################################################################


#########################################################
# Mouse Moved Portion
#########################################################

    def mouseMoved(self, event):
        checkUsername = getCurrentUser()[0]
        if (self.username != checkUsername):
            self.resetUserSettings()
        if self.showExercises:
            self.start = 1
            for i in range(len(self.workoutList)):
                self.getWorkoutDescriptionTotal(i,event)
            (headerX1,headerX2,headerY1,headerY2) = ((1/4)*self.width,(3/4)*self.width,
                                                    (1/16)*self.height-self.heightAdjuster,
                                                    (2/16)*self.height-self.heightAdjuster)
            if self.checkMoveBox(event.x,event.y,headerX1,headerX2,headerY1,headerY2):
                self.curWorkoutDescription = ""
                self.showWorkoutDescription = False

    def resetUserSettings(self):
        # Resets the user settings to match that of the current user
        # Used when changing the username 
        [self.username, self.password, self.gender, 
        self.weight, self.age, self.activityLevel] = getCurrentUser()
        self.workoutMultiplier = 1

    def getWorkoutDescriptionTotal(self,num,event):
        # Gets all the workout descriptions and allows the user
        # to view each description
        exercise = self.workoutList[num][0]
        (x1,x2,y1,y2) = ((1/4)*self.width,(3/4)*self.width,(self.start/16)*self.height,((self.start+1)/16)*self.height)
        if self.checkMoveBox(event.x,event.y,x1,x2,y1,y2):
            self.showWorkoutDescription = True
            self.workoutDescription = self.getWorkoutDescriptionList(self.workoutList[num][1])
        self.start += 1

    def getWorkoutDescriptionList(self,text):
        # Gets the workout description and splits the line if
        # it is too long
        self.curWorkoutDescription = (text.split("."))
        for i in range(len(self.curWorkoutDescription)):
            line = self.curWorkoutDescription[i]
            if (len(line)) > 130:
                self.adjustWorkoutLine(line,i)
        return self.curWorkoutDescription 
    
    def adjustWorkoutLine(self,line,num):
        # Adjusts the lines of the workout that are too long
        words = line.split(" ")
        mid = len(words)//2
        frontHalf = words[:mid]
        backHalf = words[mid:]
        self.curWorkoutDescription.pop(num)
        self.curWorkoutDescription.insert(num,frontHalf)
        self.curWorkoutDescription.insert(num+1,backHalf)

    def checkMoveBox(self,x,y,x1,x2,y1,y2):
        # Checks to see if the user clicks on the space between 
        # the x and y bounds
        return ((x1 <= x <= x2) and (y1 <= y <= y2))



#########################################################
# Mouse Pressed Portion
#########################################################

    def mousePressed(self, event):
        if (not self.showExercises):
            (bottomX1,bottomX2,bottomY1,bottomY2) = generixBoxDimensions.lowerBoxDimensions(self)
            (intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2) = (0,(1/4)*self.width,(6/8)*self.height,(7/8)*self.height)
            (categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2) = ((1/4)*self.width,(1/2)*self.width,(6/8)*self.height,(7/8)*self.height)
            (backX1,backX2,backY1,backY2) = generixBoxDimensions.upperLeftBoxDimensions(self)
            if checkClickInBox.checkInBox(event.x,event.y,bottomX1,bottomX2,bottomY1,bottomY2):
                self.getStartWorkoutOptions(event)
                # First checks if the body part and intensity are inputed
                # Then checks if the time is inputed
                # Finally, if both of those values are satisfied, then it starts a workout
            elif checkClickInBox.checkInBox(event.x,event.y,intensityBoxX1,intensityBoxX2,intensityBoxY1,intensityBoxY2):
                self.getIntensity(event)
            elif checkClickInBox.checkInBox(event.x,event.y,categoryBoxX1,categoryBoxX2,categoryBoxY1,categoryBoxY2):
                self.getBodyPart(event)
            elif checkClickInBox.checkInBox(event.x,event.y,backX1,backX2,backY1,backY2):
                self.app.setActiveMode(self.app.ReturnLoginScreen)
        else:
            (endX1,endX2,endY1,endY2) = (0,(1/4)*self.width,(7/8)*self.height,self.height)
            (pauseX1,pauseX2,pauseY1,pauseY2) = ((3/4)*self.width,self.width,(7/8)*self.height,self.height)
            if checkClickInBox.checkInBox(event.x,event.y,endX1,endX2,endY1,endY2):
                self.endWorkout()
            if checkClickInBox.checkInBox(event.x,event.y,pauseX1,pauseX2,pauseY1,pauseY2):
                self.checkTimerStatus()

    def getStartWorkoutOptions(self,event):
        # See self.getStartWorkoutOptions statement above
        self.getTime(event)
        if not self.verifyBodyPartAndIntensityInput():
            self.showWorkoutInputsIncomplete = True
            self.showWorkoutDurationIncorrect = False
        if not self.verifyTimeInput():
            self.showWorkoutInputsIncomplete = False
            self.showWorkoutDurationIncorrect = True
        if self.verifyInputs():
            self.startWorkout()

    def endWorkout(self):
        # Removes the exercises and descriptions from view
        # And show the time the user has worked out
        self.showExercises = False
        self.showWorkoutDescription = False
        self.calculateWorkoutDuration()
        self.showWorkoutDuration = True

    def calculateWorkoutDuration(self):
        # Calculates the workout duration in 1/10 seconds
        # timerDelay is at 100 because of the animation at the title screen
        minutesLeft = ((self.time)*600 - self.timer) // 600
        secondsLeft = ((self.time)*600 - self.timer) % 600
        if minutesLeft == 0:
            message = (f'Workout Canceled')
        elif self.minutes > 5:
            self.workoutMultiplier *= 1.005
            message = (f'''You finished the workout in {minutesLeft} minutes and {str(secondsLeft)[:-1]} seconds 
                                        Workout Adjusted''')
        elif secondsLeft//10 == 0:
            message = f"You finished the workout in {minutesLeft} minutes and 0{str(secondsLeft)[:-1]} seconds"
        else:
            message = f"You finished the workout in {minutesLeft} minutes and {str(secondsLeft)[:-1]} seconds"
        return message

    def verifyBodyPartAndIntensityInput(self):
        # Checks to make sure the body part and intensity are inputed before
        # the program can continue
        if ((self.bodyPart in ["legs","core","back","chest","full","plyos"]) and 
            isinstance(self.intensity,int) and (1 <= self.intensity <= 5)):
            return True

    def verifyTimeInput(self):
        # Checks to make sure the time is inputed before
        # the program can continue
        if (isinstance(self.time,int)) and (self.time >= 15):
            return True

    def verifyInputs(self):
        # Checks to ensure both programs are inputed before
        # the program can continue
        return self.verifyBodyPartAndIntensityInput() and self.verifyTimeInput()

    def startWorkout(self):
        # Starts the workout for the user
        self.showWorkoutDuration = False
        self.showWorkoutInputsIncomplete = False
        self.showWorkoutDurationIncorrect = False
        self.workoutList, self.totalCalories = workoutGenerator(getCurrentUser(),self.bodyPart,self.intensity,self.time,self.workoutMultiplier)
        self.showExercises = True
        self.setTimer()


#########################################################
# Timer Portion
#########################################################

    def setTimer(self):
        # Sets the minutes and seconds for the program
        self.timer = (self.time)*600
        self.minutes = self.timer // 600
        self.seconds = self.timer % 600

    def timerFired(self):
        # Fires the timer
        if self.showExercises:
            if not self.timerPaused:
                self.timer -= 1
                self.minutes = self.timer // 600
                self.seconds = self.timer % 600

    def checkTimerStatus(self):
        # Changes the timer to be on or off depending on user presses
        if (not self.timerPaused):
            self.timerPaused = True
        else:
            self.timerPaused = False

#########################################################
# User inputs:
#   body part they want to work on
#   intensity of the workout
#   amount of time they have to workout
#########################################################

    def getIntensity(self, event):
        # Retrieves the intensity of the workout that the user inputs
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
        # Retrieves the amount of time the user will workout for
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
        # Retrieves the bodypart that the user wants to workout
        self.bodyPart = self.getUserInput('Enter your category here \n Categories: legs, core, back, chest, full, and plyos')
        if (self.bodyPart == None):
            self.bodyPart = "Must enter category \n to continue"
        elif (self.bodyPart not in ["legs","core","back","chest","full","plyos"]):
            self.bodyPart = "Must be written \n exactly to continue"
        else:
            self.bodyPart = self.bodyPart

    def userStatsPart1(self):
        # Displays the gender and weight of the user
        self.userInfoPart1 = f'Gender: {self.gender} \n Weight: {self.weight}'
        return self.userInfoPart1

    def userStatsPart2(self):
        # Displays the age and activity level of the user
        self.userInfoPart2 = f' Age: {self.age} \n Activity Level: {self.activityLevel}'
        return self.userInfoPart2

#############################################################################
# View Portion
#############################################################################


#########################################################
# Always On
#########################################################

    def drawUserInputBoxes(self,canvas):
        self.userMessages = [f'Intensity: \n {self.intensity}',f'Category: \n {self.bodyPart}',
                            self.userStatsPart1(),self.userStatsPart2()]
        for i in range(4):
            (x1,x2,y1,y2) = ((i/4)*self.width,((i+1)/4)*self.width,(6/8)*self.height,(7/8)*self.height) 
            canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "orange2")
            inputBoxes.drawInputBoxes(self,self.userMessages[i],getFontSize.fontSize(20),x1,x2,y1,y2,canvas)


#########################################################
# Before Workout
#########################################################

    def drawBottomBoxPreWorkout(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "medium sea green")
        inputBoxes.drawInputBoxes(self,"Generate Workout",getFontSize.fontSize(40),x1,x2,y1,y2,canvas)

    def drawWorkoutDurationIncorrect(self,canvas):
        canvas.create_text(self.width/2,self.height/2,text = 'Must be at least 15 minutes', fill = "red", font = getFontSize.fontSize(40))

    def drawWorkoutInputsIncomplete(self,canvas):
        canvas.create_text(self.width/2,self.height/2,text = 'Must enter category \n and intensity to continue', fill = "red", font = getFontSize.fontSize(40))

    def drawBackButton(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.upperLeftBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.backButtonScaled))


#########################################################
# During Workout
#########################################################

    def drawHeader(self,canvas):
        (x1,x2,y1,y2) = ((1/4)*self.width,(3/4)*self.width,(1/16)*self.height-self.heightAdjuster,(2/16)*self.height-self.heightAdjuster)
        inputBoxes.drawInputBoxes(self,f"Estimated Calories Burned: {self.totalCalories}",getFontSize.fontSize(30),x1,x2,y1,y2,canvas)

    def drawWorkoutText(self,canvas):
        start = 2
        for i in range(len(self.workoutList)):
            exercise = self.workoutList[i][0]
            (x1,x2,y1,y2) = ((2/5)*self.width,(3/5)*self.width,(start/16)*self.height - self.heightAdjuster,((start+1)/16)*self.height - self.heightAdjuster)
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

    def drawPauseWorkoutButton(self,canvas):
        (x1,x2,y1,y2) = (0,(1/4)*self.width,(7/8)*self.height,self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "firebrick1")
        inputBoxes.drawInputBoxes(self,"End Workout",getFontSize.fontSize(32),x1,x2,y1,y2,canvas)

    def drawTimerWorkoutButton(self,canvas):
        (x1,x2,y1,y2) = ((1/4)*self.width,(3/4)*self.width,(7/8)*self.height,self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "green yellow")
        if self.seconds < 10:
            inputBoxes.drawInputBoxes(self,f'Time Remaining: {self.minutes}:00{str(self.seconds)[:-1]}',getFontSize.fontSize(32),x1,x2,y1,y2,canvas)
        elif self.seconds < 100:
            inputBoxes.drawInputBoxes(self,f'Time Remaining: {self.minutes}:0{str(self.seconds)[:-1]}',getFontSize.fontSize(32),x1,x2,y1,y2,canvas)
        else:
            inputBoxes.drawInputBoxes(self,f'Time Remaining: {self.minutes}:{str(self.seconds)[:-1]}',getFontSize.fontSize(32),x1,x2,y1,y2,canvas)

    def drawEndWorkoutButton(self,canvas):
        (x1,x2,y1,y2) = ((3/4)*self.width,self.width,(7/8)*self.height,self.height)
        canvas.create_rectangle(x1,y1,x2,y2, outline = None, fill = "peach puff")
        if self.timerPaused:
            inputBoxes.drawInputBoxes(self,"  Resume \n Workout",getFontSize.fontSize(32),x1,x2,y1,y2,canvas)
        else:
            inputBoxes.drawInputBoxes(self,"  Pause \n Workout",getFontSize.fontSize(32),x1,x2,y1,y2,canvas)

    def drawBottomBoxDuringWorkout(self,canvas):
        self.drawPauseWorkoutButton(canvas)
        self.drawTimerWorkoutButton(canvas)
        self.drawEndWorkoutButton(canvas)

    def drawWorkoutDurationMessage(self,canvas):
        canvas.create_text(self.width/2,self.height/2,text = f'{self.calculateWorkoutDuration()}', fill = "forest green", font = getFontSize.fontSize(32))

    def redrawAll(self, canvas):
        self.drawUserInputBoxes(canvas)
        if self.showExercises:
            self.drawBottomBoxDuringWorkout(canvas)
            self.drawWorkoutText(canvas)
            self.drawHeader(canvas)
        else:
            self.drawBottomBoxPreWorkout(canvas)
            self.drawBackButton(canvas)
        if self.showWorkoutDescription:
            self.drawWorkoutDescription(canvas)
        if self.showWorkoutInputsIncomplete:
            self.drawWorkoutInputsIncomplete(canvas)
        if self.showWorkoutDurationIncorrect:
            self.drawWorkoutDurationIncorrect(canvas)
        if self.showWorkoutDuration:
            self.drawWorkoutDurationMessage(canvas)