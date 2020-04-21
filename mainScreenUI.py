from cmu_112_graphics import *
from helperFunctionsUI import *
from returnLoginScreenUI import *

class MainScreen(Mode):

    


    def redrawAll(self,canvas):
        canvas.create_rectangle(100,100,300,300, outline = "black")




# class MyApp(ModalApp):
#     def appStarted(self):
#         self.MainScreen = MainScreen()
#         self.setActiveMode(self.MainScreen)

# app = MyApp(width=1000, height=800)