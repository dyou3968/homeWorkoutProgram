#############################################################################
"""
This is the main screen where the user chooses the specific body part they 
want to workout, and how much time they have.
"""
#############################################################################

from cmu_112_graphics import *
from helperFunctionsUI import *
from returnLoginScreenUI import *
from exerciseGenerator import *

class MainScreen(Mode):
    def appStarted(self):
        ([self.username, self.password, self.gender, 
        self.weight, self.age, self.activityLevel]) = self.getCurrentUser()    
        self.bodyPart = "core"
        self.intensity = None
        self.timeDuration = None


    def mousePressed(self,event):
        self.getExerciseDictionary()
        print(self.bodyPartSpecificDict)


    # Will run
    # x = WorkoutGenerator("core","high")
    # which will be an exercise workout list




#############################################################################
# User inputs:
#   body part they want to work on
#   intensity of the workout
#   amount of time they have to workout
#############################################################################

    def getUsername(self, event):
        username = self.getUserInput('Enter your username')
        if (username == None):
            self.username = "Must enter username \n to login"
        else:
            self.username = username



#############################################################################
# View Portion
#############################################################################

    #def redrawAll(self, canvas):



class MyApp(ModalApp):
    def appStarted(self):
        self.MainScreen = MainScreen()
        self.setActiveMode(self.MainScreen)

app = MyApp(width=1000, height=800)



"""
Stuff to make:

main Screen UI:

"New Workout"
    Body Part
    Intensity
    Time


Take those factors and the user profile


WorkoutGenerator()
    Outputs a workout as a list that can be completed in that time

    Outputs a workout that maximizes a specific goal:
        For MVP, make the program work so that is maximizes muscle growth

        I.e. muscle growth, weight loss (research more)

    Will probably choose a subset of the current dictionary, and then for each one,
        have it pre-set to a circuit

Min Time: 15 minutes
Max Time: 60 minutes
    




Stuff to Research;
    Max:
        Calories burned based on different factors
        Calories burned based on different exercises

    Min:
        Time

"""




# class MyApp(ModalApp):
#     def appStarted(self):
#         self.MainScreen = MainScreen()
#         self.setActiveMode(self.MainScreen)

# app = MyApp(width=1000, height=800)