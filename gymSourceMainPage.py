from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Beautiful Soup Documentation Taken from 
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class

# url Request taken from
# https://docs.python.org/3/library/urllib.request.html

def retrieveURLInfo():
    # Gets the URL for gymsource and returns the html for the categories
    my_url = "https://www.gymsource.com/equipment"
    uClient = uReq(my_url, data = None)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    items = page_soup.findAll("div", {"class": "category-section"})
    return items

def getGymSourceCategoriesAndItemsFromHTML(htmlText):
    # Takes in HTML, parses through the material, and returns a dictionary
    # Mapping each category to the equipment
    categoryDict = dict()
    for i in range(len(htmlText)):
        typeOfExercise = htmlText[i]
        category = typeOfExercise.find("div", {"class": "category-header"})
        exercises = htmlText[i]
        machines = exercises.find("div", {"class":"category-items"})
        machineText = machines.text.splitlines()
        equipmentList= (" ".join(machineText)).strip().split("  ")
        revisedEquipmentList = recursiveRemoveExtraWhiteSpace(equipmentList)
        categoryTitle = category.h2.text
        categoryDict[categoryTitle] = revisedEquipmentList
    return categoryDict

def recursiveRemoveExtraWhiteSpace(L):
    # Takes in a list with extra entries between the values
    # And recursively returns a list with the extra whitespace removed
    if L == []:
        return []
    else:
        firstItem = L[0]
        rest = recursiveRemoveExtraWhiteSpace(L[1:])
        if firstItem == "":
            return rest
        else:
            return [firstItem.strip()] + rest