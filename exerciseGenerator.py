#############################################################################
"""
This is the exercise generator that takes the different parameters and creates
the workout.
"""
"""
# Body Parts: legs, core, back, chest, full, and plyos
# Legs: 26 exercises
# Core: 22 exercises
# Back: 10 exercises
# Chest: 18 exercises
# Full: 11 exercises
# Plyos: 13 exercises
"""
# Exercise Information Taken from
# https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp
# I will set the MET = 6 for these activities
# Energy expenditure (calories/minute) = .0175 x MET (from table) x weight (in kilograms)

#############################################################################
import random
from exercisesDict import *
from exerciseBodyPartSpecificExercises import *
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
    # Returns the dictionary of all the exercises of that specific body part
    exerciseCategoryDict = convertHTMLToDictionary(key = None)
    bodyPartSpecificDict = getOnlyExercises(exerciseCategoryDict,bodyPart)
    return bodyPartSpecificDict

def cleanUpExercise(exercise):
    # Takes in the exercise from the dictionary and removes all the numbers and white space
    entries = exercise.split(" ")
    return entries[1] 

def getExerciseAndDescriptions(bodyPart):
    # Returns all the exercises in a 2dlist, with the exercise in the first index
    # And the descriptions the second
    bodyPartSpecificDict = getExerciseDictionary(bodyPart)
    exerciseAndDescriptionList = []
    for key in bodyPartSpecificDict:
        innerDict = bodyPartSpecificDict[key]
        for exercise in innerDict:
            cleanedExercise = cleanUpExercise(exercise)
            description = innerDict[exercise][0]
            exerciseAndDescriptionList.append([cleanedExercise,description])
    return exerciseAndDescriptionList

def pickRandomExercises(numExercises,bodyPart):
    # Picks a number of exercises from the complete list of that set
    exerciseAndDescriptionList = getExerciseAndDescriptions(bodyPart)
    random.shuffle(exerciseAndDescriptionList)
    if (len(exerciseAndDescriptionList[:numExercises]) != numExercises):
        return "Not enough exercises in that category"
    return exerciseAndDescriptionList[:numExercises]

def getGenderMultiplier(gender):
    # Genders: Male, Female, and Other
    if gender == "male":
        return 1.4
    elif gender == "female":
        return 1.2
    else:
        return 1.3

def getNumRepsForExercise(exercise,gender,weight,age,activityLevel,intensity):
    #  I want to maximize the number of reps based on these factors
    gendermultiplier = getGenderMultiplier(gender)
    constraint1 = 100 - int(age)
    constraint2 = int(round(int(weight)/2.2)) # Weight in kg
    constraint3 = int(0.0175 * 6 * (int(weight)/2.2) * gendermultiplier * 2 * (1 + random.random()))
    """
    Note: 6 is the MET. For more information, click the link above
    """
    coefficientX1L1 = random.randrange(4,7) - int(activityLevel)
    coefficient21L1 = random.randrange(6,8) - int(intensity)
    coefficientX1L2 = random.randrange(4,7) - int(activityLevel)
    coefficient21L2 = random.randrange(6,8) - int(intensity)
    problem = f'''
Maximize: x1 + x2 = z
Constraints:
{coefficientX1L1}x1 + {coefficient21L1}x2 <= {constraint1}
{coefficientX1L2}x1 + {coefficient21L2}x2 <= {constraint2}
x2 <= {constraint3}
x1, x2 >= 0
'''
    solution = getOptimizedValue(problem)
    return solution

def workoutGenerator(user,bodyPart,intensity):
    # Get the number of reps for that exercise
    exerciseList = pickRandomExercises(7,bodyPart)
    (gender,weight,age,activityLevel) = (user[2],user[3],user[4],user[5])
    workout = []
    for i in range(len(exerciseList)):
        exercise = exerciseList[i][0]
        description = exerciseList[i][1]
        numReps = getNumRepsForExercise(exercise,gender,weight,age,activityLevel,intensity)
        exerciseReps = (f'{numReps} reps of {exercise}')
        workout.append([exerciseReps,description])
    return workout
