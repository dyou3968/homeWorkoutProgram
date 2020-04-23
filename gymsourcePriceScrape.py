#############################################################################
"""
This program scrapes the Gym Source price page for the name and price 
of each item.
"""
#############################################################################

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Beautiful Soup Documentation Taken from 
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class

# url Request taken from
# https://docs.python.org/3/library/urllib.request.html

def cleanUpPrices(price):
    #Inputs a string and returns the price as a float
    intPriceStr = ""
    for c in price:
        if (c.isdigit()) or (c == "."):
            intPriceStr += c
    intPrice = '${:,.2f}'.format(float(intPriceStr))
    return intPrice

def getPrices():
    # Gets the name and the price of all the items and returns a 2d list
    # With each item with its price
    my_url = "https://www.gymsource.com/equipment/mats?type=residential"
    # Opening connection
    uClient = uReq(my_url, data = None)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    items = page_soup.findAll("div", {"class": "flex"})
    totalEntries = [['Item','Price']]
    for i in range(len(items)):
        currentItem = items[i]
        currentName = currentItem.find("div", {"class":"card-center"})
        currentName = "".join(currentName.text.split())
        currentPrice = currentItem.find("div", {"class":"card-content"})
        currentPrice = "".join(currentPrice.div.text.split())
        newPrice = cleanUpPrices(currentPrice)
        currentEntry = [currentName,newPrice]
        totalEntries.append(currentEntry)
    return totalEntries