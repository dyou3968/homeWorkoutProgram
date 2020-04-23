#############################################################################
"""
This is the new user information screen where the user inputs their information.
The information is then stored into a txt file, which will be used by the other 
files.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *

class NewUserInformationScreen(Mode):
    def appStarted(self):
        self.rows = 6
        self.cols = 2
        self.margin = self.width/10
        self.selection = (-1.-1)
        self.username = "Click here"
        self.password = "Click here"
        self.gender = "Click here"
        self.weight = "Click here"
        self.age = "Click here"
        self.activityLevel = "Click here"

        self.someEntriesEmpty = False

#############################################################################
# Control Portion
#############################################################################


############################################################
# From https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
############################################################

    def mousePressed(self, event):
        (row, col) = viewToModel.getCell(self,event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.selection == (row, col)):
            self.selection = (-1, -1)
        else:
            self.selection = (row, col)

############################################################

        if self.selection == (0,1) :
            self.getUsername(event)
        elif self.selection == (1,1):
             self.getPassword(event)
        elif self.selection == (2,1):
             self.getGender(event)
        elif self.selection == (3,1):
             self.getWeight(event)
        elif self.selection == (4,1):
             self.getAge(event)
        elif self.selection == (5,1):
             self.getActivityLevel(event)
        (backX1,backX2,backY1,backY2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (nextX1,nextX2,nextY1,nextY2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,backX1,backX2,backY1,backY2):
            self.app.setActiveMode(self.app.NewLoginScreen)
        if checkClickInBox.checkInBox(event.x, event.y,nextX1,nextX2,nextY1,nextY2):
            self.potentialOutcomesOfLogin()

    def potentialOutcomesOfLogin(self):
        if "Click here" not in self.getUserInformation():
            self.someEntriesEmpty = False
            self.addUserInformation("userProfile.txt")
            print("User added to database")
            self.app.setActiveMode(self.app.ReturnLoginScreen)
        else:
            self.someEntriesEmpty = True

#############################################################################


#############################################################################
# Add User Information to Text File

# Inspiration from: 
# https://github.com/dyou3968/o-nlogn-/blob/master/SpeechRecog/todoListFunction.py
# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
#############################################################################

    def textToFile(self,path,text):
        file = open(r"userProfile.txt","w+")
        file.write(text)
        file.close()

    def getUserList(self,path):
        with open(path, "rt") as f:
            return f.read()

    def addUser(self,path,user):
        users = self.getUserList("userProfile.txt")
        users += user + "\n"
        self.textToFile(path,users)
        return None

    def addUserInformation(self,path):
        return self.addUser(path,str(self.userInfo))

    def getUserInformation(self):
        self.userInfo = [self.username,self.password,self.gender,
                        self.weight,self.age,self.activityLevel]
        return self.userInfo


#############################################################################


#############################################################################
# User Inputs
#############################################################################

    def getUsername(self, event):
        username = self.getUserInput('Enter your username')
        if (username == None):
            self.username = "Must enter username \n to login"
        else:
            self.username = username

    def getPassword(self, event):
        password = self.getUserInput('Enter your password')
        if (password == None):
            self.password = "Must enter password \n to login"
        else:
            self.password = password

    def getGender(self, event):
        gender = self.getUserInput('Enter your gender')
        if (gender == None) or (gender.lower() not in ['male','female','other']):
            self.gender = "Please enter gender to login"
        else:
            self.gender = gender.lower()

    def getWeight(self, event):
        weight = self.getUserInput('Enter your weight in lbs')
        try:
            self.weight = int(weight)
            if (self.weight == None):
                self.weight = "Must enter weight to login"            
            else:
                self.weight = weight
        except:
            self.weight = "Weight must be \n a whole number"

    def getAge(self, event):
        age = self.getUserInput('Enter your age')
        try:
            self.age = int(age)
            if (self.age == None):
                self.age = "Must enter age to login"            
            else:
                self.age = age
        except:
            self.age = "Age must be \n a whole number"

    def getActivityLevel(self, event):
        message = '''
        Enter your activity level from 1 to 3, 
        with 1 being the least active 
        and 3 being the most active.
            1: Low Activity Level 
            2: Moderate Activity Level
            3: High Activity Level
        '''
        activityLevel = self.getUserInput(message)
        try:
            self.activityLevel = int(activityLevel)
            if (self.activityLevel == None):
                self.activityLevel = "Must enter activity level to login"            
            elif (not 1 <= self.activityLevel <= 3):
                self.activityLevel = "Must be between \n 1 and 3 inclusive"
            else:  
                self.activityLevel = activityLevel
        except:
            self.activityLevel = "Activity level must be \n a whole number"

#############################################################################


#############################################################################
# View Portion
#############################################################################

    def drawInputBoxes(self,text,font,x1,x2,y1,y2,canvas):
        canvas.create_text((x1+x2)/2,(y1+y2)/2,text = text, font = font)

    def createTextInBoxes(self,row,col,font,x1,x2,y1,y2,canvas):
        # Default Column
        if (row == 0) and (col == 0):
            self.drawInputBoxes("Username",font,x1,x2,y1,y2,canvas)
        if (row == 1) and (col == 0):
            self.drawInputBoxes("Password",font,x1,x2,y1,y2,canvas)
        if (row == 2) and (col == 0):
            self.drawInputBoxes("Gender",font,x1,x2,y1,y2,canvas)
        if (row == 3) and (col == 0):
            self.drawInputBoxes("Weight",font,x1,x2,y1,y2,canvas)
        if (row == 4) and (col == 0):
            self.drawInputBoxes("Age",font,x1,x2,y1,y2,canvas)
        if (row == 5) and (col == 0):
            self.drawInputBoxes("Activity Level",font,x1,x2,y1,y2,canvas)
        # User Input column
        if (row == 0) and (col == 1):
            self.drawInputBoxes(self.username,font,x1,x2,y1,y2,canvas)
        if (row == 1) and (col == 1):
            self.drawInputBoxes(self.password,font,x1,x2,y1,y2,canvas)
        if (row == 2) and (col == 1):
            self.drawInputBoxes(self.gender,font,x1,x2,y1,y2,canvas)
        if (row == 3) and (col == 1):
            self.drawInputBoxes(self.weight,font,x1,x2,y1,y2,canvas)
        if (row == 4) and (col == 1):
            self.drawInputBoxes(self.age,font,x1,x2,y1,y2,canvas)
        if (row == 5) and (col == 1):
            self.drawInputBoxes(self.activityLevel,font,x1,x2,y1,y2,canvas)

    def createTextBoxes(self,canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = modelToView.getCellBounds(self,row,col)
                font = "Times_New_Roman 28 bold"
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
        if (self.someEntriesEmpty):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red", 
                            text = "Must enter all entries to continue", font = getFontSize.fontSize(30))
