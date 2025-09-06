import datetime

#####
# ref https://www.w3schools.com/python/python_datetime.asp
#
def GetCurrentDateTimeFormatted ():

    currentDateTime = datetime.datetime.now()
    date_string = currentDateTime.strftime("%m/%d/%Y %H:%M:%S")

    return date_string

