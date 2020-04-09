


# class Intensity(object):
#     def __init__(self, intensity):
#         self.intensity = intensity

    #def intensityCalculator(self):

"""
Intensity should be a number from 1 to 5,
with 1 being the most intense
"""

class WorkoutGenerator(object):
    def __init__(self, name, weight, gender, age, activity, bodyPart, intensity):
        self.name = name
        # Full name
        self.weight = weight
        # Weight inlbs
        self.gender = gender
        # Male, female, or other
        self.age = age
        # Age
        self.activity = activity
        # Level of exercise beforehand
        # 1 is the highest, 5 is the lowest
        self.bodyPart = bodyPart
        # Type of workout
        self.intensity = intensity
        # 1 is the most intense, 5 is the least intense
        self.workoutDuration = 20 # minutes
        self.restTime = 30 # seconds of rest between each set
        self.reps = 20 # Should be based on the exercise, and everything else
    



legWorkout = WorkoutGenerator("David You", 160,"male",19,"medium","legs","high")

"""
Input: legWorkout = WorkoutGenerator("David You", 160,"male",19,"medium","legs","high")

Output:
As of right now, print out the list of exercises and the workouts


"""