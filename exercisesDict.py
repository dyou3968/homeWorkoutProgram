#############################################################################
"""
This program scrapes the travel strong website for all the exercises 
and returns the information as a dictionary.
"""
#############################################################################

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Beautiful Soup Documentation taken from 
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class

# url Request taken from
# https://docs.python.org/3/library/urllib.request.html

def getWorkoutData():
    # Receives the 100 workout exercises from this website
    url = "https://travelstrong.net/bodyweight-exercises/#plyos"
    # Opening connection
    uClient = uReq(url, data = None)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    items = page_soup.findAll("div", {"class": "entry-content"})[0]
    categories = items.findAll("p")
    return categories

def cleanUpText(text):
    # Returns a cleaned up string without the "\xa0" values from web scraping
    return " ".join(text.split("\xa0"))

def convertHTMLToDictionary(key = None):
    # Converts the html code into a Python dictionary
    data = getWorkoutData()
    exerciseCategoryDict = dict()
    for i in range(len(data)-1):
        exerciseName = data[i].text
        exerciseName = cleanUpText(exerciseName)
        exerciseDescriptions = data[i+1].text
        exerciseDescriptions = cleanUpText(exerciseDescriptions)
        topic = (data[i].find("a",id=True))
        if topic != None:
            key = topic['id']
            exerciseCategoryDict[key] = dict()
        if exerciseName != "":
            if exerciseName[0].isdigit():
                link = (data[i].find("a", href = True))['href']
                exerciseCategoryDict[key][exerciseName] = [exerciseDescriptions,link]
    return exerciseCategoryDict