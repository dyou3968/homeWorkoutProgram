from cmu_112_graphics import *
from helperFunctionsUI import *
from startScreenUI import *
from newLoginScreenUI import *
from returnLoginScreenUI import *
from newUserInformationScreenUI import *


class MyApp(ModalApp):
    def appStarted(self):
        self.StartScreen = StartScreen()
        self.ReturnLoginScreen = ReturnLoginScreen()
        self.NewLoginScreen = NewLoginScreen()
        self.NewUserInformationScreen = NewUserInformationScreen()
        #self.MainScreen = MainScreen()
        self.setActiveMode(self.StartScreen)

app = MyApp(width=1000, height=800)