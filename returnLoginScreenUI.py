#############################################################################
"""
This is the new returning information screen where the user inputs their username
and password. The program checks to see if the username and password are contained
in the text file, and if so takes that person's "profile". The new user login
screen also maps to this page for the user to login.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *
from mainScreenUI import *

class ReturnLoginScreen(Mode):
    def appStarted(self):
        self.rows = 2
        self.cols = 2
        self.margin = self.width/8
        self.selection = (-1.-1)
        self.username = "Click here"
        self.password = "Click here"

        # Boolean Conditions
        self.someEntriesEmpty = False
        self.userInData = True
        self.correctPassword = True

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

#########################################################
# From https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#########################################################

    def mousePressed(self, event):
        (row, col) = viewToModel.getCell(self,event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.selection == (row, col)):
            self.selection = (-1, -1)
        else:
            self.selection = (row, col)

#########################################################

        if self.selection == (0,1) :
            self.getUsername(event)
        elif self.selection == (1,1):
             self.getPassword(event)
        (backX1,backX2,backY1,backY2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        (nextX1,nextX2,nextY1,nextY2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        if checkClickInBox.checkInBox(event.x, event.y,backX1,backX2,backY1,backY2):
            self.app.setActiveMode(self.app.StartScreen)
        if checkClickInBox.checkInBox(event.x, event.y,nextX1,nextX2,nextY1,nextY2):
            self.potentialOutcomesOfLogin()

    def potentialOutcomesOfLogin(self):
        # Enters the workout screen if the user has entered 
        # All the information correctly
        if "Click here" not in self.getUsernameAndPassword():
            userData = self.getUserData("userProfile.txt") #2d List of the all the user data
            self.someEntriesEmpty = False
            if (not self.checkIfUserInData(userData, self.username)):
                self.correctPassword = True
                self.userInData = False
            elif (not self.checkPasswordMatch(userData,self.password)):
                self.userInData = True
                self.correctPassword = False
            else:
                self.removeOtherUsers("currentUser.txt")
                self.addUserInformation("currentUser.txt", self.userProfile(userData,self.username))          
                self.app.setActiveMode(self.app.MainScreen)
        else:
            self.someEntriesEmpty = True

#########################################################
# Get User Inputs
#########################################################

    def getUsername(self, event):
        username = self.getUserInput('Enter your username')
        if (username == None):
            self.username = "Must enter username to login"
        else:
            self.username = username

    def getPassword(self, event):
        password = self.getUserInput('Enter your password')
        if (password == None):
            self.password = "Must enter password to login"
        else:
            self.password = password

#########################################################
# Retrieves the user information from the txt file
# First, it checks to see if the username is in the file
# Then, it checks if the password matches the password on file

# Inspiration from:
# https://github.com/dyou3968/o-nlogn-/blob/master/SpeechRecog/todoListFunction.py
# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
#########################################################

    def getUserList(self,path):
        with open(path,'rt') as f:
            return f.read()

    def getUserData(self,path):
        userProfiles = self.getUserList(path)
        userList = []
        for user in userProfiles.splitlines():
            modifiedUser = self.cleanUpUserData(user)
            userList.append(modifiedUser)
        return userList

    def cleanUpUserData(self,user):
        # Takes in the unmodified string from the txt file and returns a list
        # This list will be added to the userList, so it will create a 2d list
        user = user[1:-1]
        userInfo = user.split(",")
        modifiedUserInfoList = []
        for entry in userInfo:
            entry = entry.strip()
            entry = entry[1:-1]
            modifiedUserInfoList.append(entry)
        return modifiedUserInfoList

    def getUsernameAndPassword(self):
        self.userInfo = [self.username,self.password]
        return self.userInfo

    def checkIfUserInData(self,userData, username):
        # Checks if the user is in the text file 'userProfile.txt'
        rows = len(userData)
        for row in range(rows):
            dataUsername = userData[row][0]
            if dataUsername == username:
                return True
        return False

    def userProfile(self,userData,username):
        # Checks if the username entered matches the username in the 
        # 'userProfile.txt' file
        rows = len(userData)
        for row in range(rows):
            dataUsername = userData[row][0]
            if dataUsername == username:
                return userData[row]
        return None

    def checkPasswordMatch(self, userData, password):
        # Checks if the password entered matches the password in the
        # 'userProfile.txt' file
        rows = len(userData)
        for row in range(rows):
            dataPassword = userData[row][1]
            if dataPassword == password:
                return True
        return False

    def addUser(self,path,user):
        # Adds the user into the 'userProfile.txt' file
        users = self.getUserList(path)
        users += user + "\n"
        self.textToFile(path,users)
        return None

    def textToFile(self,path,text):
        # Writes text in the file
        file = open(r"currentUser.txt","w+")
        file.write(text)
        file.close()

    def addUserInformation(self,path,currentUser):
        return self.addUser(path,str(currentUser))

    def removeOtherUsers(self,path):
        self.textToFile(path,"")

#############################################################################
# View Portion
#############################################################################

    def drawTextBoxes(self,canvas):
        textList = [["Username",self.username],["Password",self.password]]
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = modelToView.getCellBounds(self,row,col)
                text = textList[row][col]
                inputBoxes.drawInputBoxes(self,text,getFontSize.fontSize(36),x1,x2,y1,y2,canvas)
                canvas.create_rectangle(x1,y1,x2,y2, outline = "black")

    def drawNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.nextButtonScaled))

    def drawBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        cx,cy = (x1+x2)/2,(y1+y2)/2
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(self.backButtonScaled))

    def drawMessages(self,canvas):
        if (self.someEntriesEmpty):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "Must enter all entries to continue", font = getFontSize.fontSize(30))
        if (not self.userInData):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "User not in data", font = getFontSize.fontSize(30))
        if (not self.correctPassword):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "Incorrect Password", font = getFontSize.fontSize(30))

    def redrawAll(self,canvas):
        self.drawTextBoxes(canvas)
        self.drawNextBox(canvas)
        self.drawBackBox(canvas)
        self.drawMessages(canvas)