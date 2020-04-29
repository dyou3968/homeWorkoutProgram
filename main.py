#############################################################################
"""
This is the main file that will run the entire program. I will import
all the different files into this file.
"""
#############################################################################

from cmu_112_graphics import *
from startScreenUI import *
from newLoginScreenUI import *
from returnLoginScreenUI import *
from newUserInformationScreenUI import *
from mainScreenUI import *

class MyApp(ModalApp):
    def appStarted(self):
        self.StartScreen = StartScreen()
        self.ReturnLoginScreen = ReturnLoginScreen()
        self.NewLoginScreen = NewLoginScreen()
        self.NewUserInformationScreen = NewUserInformationScreen()
        self.MainScreen = MainScreen()
        self.setActiveMode(self.StartScreen)
        self.timerDelay = 100
        
app = MyApp(width=1000, height=800)
