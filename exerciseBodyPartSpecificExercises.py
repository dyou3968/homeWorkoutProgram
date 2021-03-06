#############################################################################
"""
This program takes the exercise dictionary from exerciseDict.py and cleans up
all the data in a way that it can be easier read by Python and me. It returns 
a cleaned up version of the dictionary of exercises, and combines the 
calves, thighs, and glutes portion of the exercises into one "legs" dictionary.
"""
#############################################################################

from exercisesDict import *

exerciseCategoryDict = convertHTMLToDictionary(key = None)

def getExerciseTypeAndName(d):
    # Takes the dictionary of exercise categories, exercises, descrptions, and links
    # And returns a new dictionary mapping the original key to a list of the
    # exercises only
    bodyWeightExerciseDict = dict()
    for key in d:
        bodyWeightExerciseDict[key] = []
        for secondKey in d[key]:
            exercise = cleanUpExerciseNames(secondKey)
            bodyWeightExerciseDict[key].append(exercise)
    return bodyWeightExerciseDict

def cleanUpExerciseNames(text):
    # Takes in an exercise and removes nonessential text
    newText = ""
    for c in text:
        if (c.isalpha()) or (c == "-") or (c.isspace()):
            newText += c
    return newText.strip()

def getOnlyLegExercises(d):
    # Inputs the exercise dictionary and returns a dictionary
    # Of only leg exercises
    legWorkoutDict = dict()
    legs = ["calves","thighs","glutes"]
    for bodyPart in legs:
        for key in d:
            if (key == bodyPart):
                legWorkoutDict[key] = d[key]
    return legWorkoutDict

def cleanUpLegDict(d):
    legWorkoutDict = getOnlyLegExercises(d)
    exercises = legWorkoutDict["glutes"]
    messedUpKey = "27. Single-Leg Shoulders-and-Feet-Elevated Hip Raise"
    del exercises[messedUpKey]
    return legWorkoutDict

def getOnlyExercises(d,bodypart):
    # Works for core, back, chest, full, and plyos
    if bodypart == "legs":
        return cleanUpLegDict(d)
    individualExerciseDict = dict()
    for key in d:
        if key == bodypart:
            individualExerciseDict[key] = d[key]
    return individualExerciseDict