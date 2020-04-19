from newUserInformationScreenUI import *

class userProfileInformation(object):
    print('a')
    def getInformation(self):
        print('b')
        information = NewUserInformationScreen.getUserInformation()
        if "Click here" not in information:
            return information


print(userProfileInformation.getInformation())