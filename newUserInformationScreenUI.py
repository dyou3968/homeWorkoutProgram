#############################################################################
"""
This is the new user information screen where the user inputs their information.
The information is then stored into a txt file, which will be used by the other 
files.
"""

# Tools and inspiration taken from 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassingApp
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

        # Boolean Conditions
        self.someEntriesEmpty = False

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

    def createTextBoxes(self,canvas):
        self.textList = [["Username",self.username],["Password",self.password],["Gender",self.gender],
                        ["Weight",self.weight],["Age",self.age],["Activity Level", self.activityLevel]]
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = modelToView.getCellBounds(self,row,col)
                font = "Times_New_Roman 28 bold"
                text = self.textList[row][col]
                inputBoxes.drawInputBoxes(canvas,text,getFontSize.fontSize(32),x1,x2,y1,y2,canvas)
                canvas.create_rectangle(x1,y1,x2,y2, outline = "black")

    def createNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.nextButtonScaled))

    def createBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.backButtonScaled))


    def redrawAll(self,canvas):
        self.createTextBoxes(canvas)
        self.createNextBox(canvas)
        self.createBackBox(canvas)
        if (self.someEntriesEmpty):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red", 
                            text = "Must enter all entries to continue", font = getFontSize.fontSize(30))


# class MyApp(ModalApp):
#     def appStarted(self):
#         self.NewUserInformationScreen = NewUserInformationScreen()
#         self.setActiveMode(self.NewUserInformationScreen)
#         self.timerDelay = 1000

# app = MyApp(width=1000, height=800)