#############################################################################
"""
This is the new returning information screen where the user inputs their username
and password. the program checks to see if the username and password are contained
in the txt file, and if so takes that person's "profile". The new user login
screen also maps to this page for the user to login.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *

class ReturnLoginScreen(Mode):
    def appStarted(self):
        self.rows = 2
        self.cols = 2
        self.margin = self.width/8
        self.selection = (-1.-1)
        self.username = "Click here"
        self.password = "Click here"

        self.someEntriesEmpty = False
        self.userInData = True
        self.correctPassword = True
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
                self.addUserInformation("currentUser.txt", self.UserProfile(userData,self.username))            
                self.app.setActiveMode(self.app.MainScreen)
                
        else:
            self.someEntriesEmpty = True

#############################################################################
# Get User Inputs
#############################################################################

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


#############################################################################


#############################################################################
# Retrieves the user information from the txt file
# First, it checks to see if the username is in the file
# Then, it checks if the password matches the password on file

# Inspiration from:
# https://github.com/dyou3968/o-nlogn-/blob/master/SpeechRecog/todoListFunction.py
# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
#############################################################################

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
        rows = len(userData)
        for row in range(rows):
            dataUsername = userData[row][0]
            if dataUsername == username:
                return True
        return False

    def checkPasswordMatch(self, userData, password):
        rows = len(userData)
        for row in range(rows):
            dataPassword = userData[row][1]
            if dataPassword == password:
                return True
        return False

    def UserProfile(self,userData,username):
        rows = len(userData)
        for row in range(rows):
            dataUsername = userData[row][0]
            if dataUsername == username:
                return userData[row]
        return None

    def addUser(self,path,user):
        users = self.getUserList(path)
        users += user + "\n"
        self.textToFile(path,users)
        return None

    def textToFile(self,path,text):
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

    def createTextInBoxes(self,row,col,font,x1,x2,y1,y2,canvas):
            if (row == 0) and (col == 0):
                inputBoxes.drawInputBoxes(self,"Username",font,x1,x2,y1,y2,canvas)
            if (row == 1) and (col == 0):
                inputBoxes.drawInputBoxes(self,"Password",font,x1,x2,y1,y2,canvas)
            # User Input column
            if (row == 0) and (col == 1):
                inputBoxes.drawInputBoxes(self,self.username,font,x1,x2,y1,y2,canvas)
            if (row == 1) and (col == 1):
                inputBoxes.drawInputBoxes(self,self.password,font,x1,x2,y1,y2,canvas)

    def createTextBoxes(self,canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                (x1, y1, x2, y2) = modelToView.getCellBounds(self,row,col)
                font = "Times_New_Roman 36 bold"
                self.createTextInBoxes(row,col,font,x1,x2,y1,y2,canvas)
                canvas.create_rectangle(x1,y1,x2,y2, outline = "black")

    def createNextBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerRightBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        inputBoxes.drawInputBoxes(self,"Next","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def createBackBox(self,canvas):
        (x1,x2,y1,y2) = generixBoxDimensions.lowerLeftBoxDimensions(self)
        canvas.create_rectangle(x1,y1,x2,y2, outline = "black")
        inputBoxes.drawInputBoxes(self,"Back","Times_New_Roman 20 bold",x1,x2,y1,y2,canvas)

    def redrawAll(self,canvas):
        self.createTextBoxes(canvas)
        self.createNextBox(canvas)
        self.createBackBox(canvas)
        if (self.someEntriesEmpty):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "Must enter all entries to continue", font = getFontSize.fontSize(30))
        if (not self.userInData):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "User not in data", font = getFontSize.fontSize(30))
        if (not self.correctPassword):
            canvas.create_text(self.width/2,(9/10)*self.height, fill = "red",
                            text = "Incorrect Password", font = getFontSize.fontSize(30))
