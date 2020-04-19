from cmu_112_graphics import *
from helperFunctionsUI import *
from newUserInformationScreenUI import *

class MainScreen(Mode):
    def appStarted(self):
        stats = NewUserInformationScreen.appStarted(self)


class MyApp(ModalApp):
    def appStarted(self):
        self.MainScreen = MainScreen()
        self.setActiveMode(self.MainScreen)

app = MyApp(width=1000, height=800)