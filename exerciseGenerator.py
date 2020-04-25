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
# I will set the MET = 5 for these activities

#############################################################################
import random
from exercisesDict import *
from exerciseBodyPartSpecificExercises import *
from simplexProgram import *






def roundHalfUp(d):
    # From https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


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

def caloriesBurnedPerMinuteVersion1(weight):
# Information taken from https://www.healthline.com/health/how-many-calories-do-squats-burn#calories-burned
# Calories burned per minute = .0175 x MET x weight (in kilograms)
# As stated above, the MET for these exercises will be 5
# Body Parts: legs, core, back, chest, full, and plyos
# This will act as part of constraint 1
    met = 5
    weightInKg = int(weight)/2.2
    return (0.0175*met*weightInKg)

def caloriesBurnedPerMinuteVersion2(weight):
# Information taken from https://www.health.harvard.edu/diet-and-weight-loss/calories-burned-in-30-minutes-of-leisure-and-routine-activities
# These exercises will be categorized as "calisthenics: moderate"
# This will act as part of constraint 2
    weightCalorieMultiplier = 1.08 #This number was determined using the data
    return (weightCalorieMultiplier*int(weight)/30)

def caloriesBurnedPerMinuteVersion3(weight):
# Information taken from https://www.urmc.rochester.edu/encyclopedia/content.aspx?ContentTypeID=41&ContentID=CalorieBurnCalc&CalorieBurnCalc_Parameters=160
# These exercises will be categorized as "calisthenics: moderate"
# This will act as part of constraint 3
    weightCalorieMultiplier = 324/60 #This number was determined using the data
    return (weightCalorieMultiplier*int(weight)/150)

def caloriesBurnedPerMinuteVersion4(weight):
# Information taken from https://www.mdanderson.org/publications/focused-on-health/How-to-determine-calorie-burn.h27Z1591413.html
# These exercises will be categorized as "resistance/weight training"
# This will act as part of constraint 4
    dataFor160lbs,datafor200lbs,datafor240lbs = 365/60,455/60,545/60
    averagedData = (dataFor160lbs + datafor200lbs*(160/200) + datafor240lbs*(160/240))/3
    return (averagedData*160/int(weight))

def maximizeNumberOfCaloriesBurnedPerExercise(exercise,gender,weight,age,activityLevel,intensity,time):
    # I want to maximize the number of calories burned per exercise
    gendermultiplier = getGenderMultiplier(gender)
    constraint1 = (roundHalfUp(caloriesBurnedPerMinuteVersion1(weight)*int(time)))
    constraint2 = (roundHalfUp(caloriesBurnedPerMinuteVersion2(weight)*int(time)))
    constraint3 = (roundHalfUp(caloriesBurnedPerMinuteVersion3(weight)*int(time)))
    constraint4 = (roundHalfUp(caloriesBurnedPerMinuteVersion4(weight)*int(time)))

    weight,age,activityLevel,intensity = int(weight),int(age),int(activityLevel),int(intensity)

    # Line 1
    coefficientX1L1 = roundHalfUp(6 - intensity)
    coefficientX2L1 = roundHalfUp((age/8)/gendermultiplier)
    # Line 2
    coefficientX1L2 = roundHalfUp(4 - activityLevel)
    coefficientX2L2 = roundHalfUp(weight/100*gendermultiplier)
    # Line 3
    coefficientX1L3 = roundHalfUp(weight/100*gendermultiplier)
    coefficientX2L3 = roundHalfUp(6 - intensity)
    # Line 4
    coefficientX1L4 = roundHalfUp((age/8)/gendermultiplier)
    coefficientX2L4 = roundHalfUp(4 - activityLevel)

    problem = f'''
Maximize: x1 + x2 = z
Constraints:
{coefficientX1L1}x1 + {coefficientX2L1}x2 <= {constraint1}
{coefficientX1L2}x1 + {coefficientX2L2}x2 <= {constraint2}
{coefficientX1L3}x1 + {coefficientX2L3}x2 <= {constraint3}
{coefficientX1L4}x1 + {coefficientX2L4}x2 <= {constraint4}
x1, x2 >= 0
''' 
    solution = getOptimizedValue(problem)*5
    return solution

def getTotalRepsPerExercise(calories,bodyPart):
    # Information taken from:
    # https://bootcampmilitaryfitnessinstitute.com/2018/02/20/how-many-calories-does-a-press-up-push-up-burn/
    # https://www.healthline.com/health/how-many-calories-do-push-ups-burn
    # https://www.livestrong.com/article/316296-how-many-calories-are-burned-per-pull-up/
    calories = calories/5
    if (bodyPart == "legs"):
        caloriesPerRep = 0.25
    elif (bodyPart == "core"):
        caloriesPerRep = 0.34
    elif (bodyPart == "back"):
        caloriesPerRep = 0.95
    elif (bodyPart == "chest"):
        caloriesPerRep = 0.30   
    elif (bodyPart == "full"):
        caloriesPerRep = 0.80     
    elif (bodyPart == "plyos"):
        caloriesPerRep = 1.2
    return int(calories/caloriesPerRep)

def workoutGenerator(user,bodyPart,intensity,time):
    # Get the total workout plan and calories
    numExercises = min(int(time)//5,7)
    exerciseList = pickRandomExercises(numExercises,bodyPart)
    (gender,weight,age,activityLevel) = (user[2],user[3],user[4],user[5])
    workout = []
    totalCalories = 0
    timePerExercise = int(time)/len(exerciseList)
    for i in range(len(exerciseList)):
        exercise = exerciseList[i][0]
        description = exerciseList[i][1]
        caloriesBurned = maximizeNumberOfCaloriesBurnedPerExercise(exercise,gender,weight,age,activityLevel,intensity,timePerExercise)
        numReps = getTotalRepsPerExercise(caloriesBurned,bodyPart)
        exerciseReps = (f'{numReps} reps of {exercise}')
        workout.append([exerciseReps,description,caloriesBurned])
        totalCalories += caloriesBurned
    return workout,totalCalories
