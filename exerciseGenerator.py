#############################################################################
"""
This is the exercise generator that takes the different parameters and creates
the workout.
"""


# Exercise Information Taken from
# https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp


#############################################################################
from exercisesDict import *
from bodyPartSpecificExercises import *
from simplexProgram import *




#############################################################################
# Retrieves the current user from currentUser.txt
#############################################################################

def getUserList(path):
    with open(path,'rt') as f:
        return f.read()

def cleanUpUserData(user):
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

def getCurrentUser():
    user = getUserList("currentUser.txt")
    for line in user.splitlines():
        modifiedUser = cleanUpUserData(line)
    return modifiedUser # ['username', 'password', 'gender', 'weight', 'age', 'activityLevel']


#############################################################################



def getExerciseDictionary(bodyPart):
    exerciseCategoryDict = convertHTMLToDictionary(key = None)
    bodyPartSpecificDict = getOnlyExercises(exerciseCategoryDict,bodyPart)
    return bodyPartSpecificDict

def getExerciseAndDescriptions(bodyPart):
    # Returns all the exercises in a list, with their descriptions
    bodyPartSpecificDict = getExerciseDictionary(bodyPart)
    innerDict = bodyPartSpecificDict[bodyPart]
    exerciseAndDescriptionOuterList = []
    for exercise in innerDict:
        exerciseAndDescriptionInnerList = []
        print(exercise)
        print(innerDict[exercise][0])


print(getExerciseAndDescriptions("core"))










"""
current User: ['david you', '1234', 'male', '160', '19', '2']


Get 6 random exercises and descriptions

MET = 6
https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp
Energy expenditure (calories/minute) = .0175 x MET (from table) x weight (in kilograms)


z = number of reps for that exercise






# Constraint 1: (100 - age)
# Constraint 2: Weight in kg
# Coeffficient of x1 = random.rand(4-6) - Activity Level for EQ1
# Coeffficient of x2 = random.rand(6-8) - Intensity Level for EQ1 (Will go from 1 to 5) 5 highest

# Coeffficient of x1 = random.rand(4-6) - Activity Level for EQ2
# Coeffficient of x2 = random.rand(6-8) - Intensity Level for EQ2 (Will go from 1 to 5) 5 highest

problem = '''
Maximize: x1 + x2 = z
Constraints:
1x1 + 2x2 <= 81
1x1 + 2x2 <= 72
x1, x2 >= 0
'''
#solution = getOptimizedValue(problem)
#print(solution)

"""



#x = (WorkoutGenerator("core","high"))
#print(x)

#def WorkoutGenerator(user, bodyPart, intensity):
    # Generates a workout based on the user's information
    # The specific bodyPart that they chose
    # And the intensity of the workout
