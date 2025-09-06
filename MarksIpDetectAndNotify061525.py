
import sys
import os
import datetime
import json
import socket

import TraceU
import FileU
import DateTimeU
import BufU

from requests import get

import smtplib
from email.mime.text import MIMEText

#####
# Application environment class.
#
class AppEnv:
    _currentComputerName = ""
    _currentDateTime = ""
    _currentFileNameNoExt = ""
    _currentFilePath = ""
    _currentDirectory = ""
    _appTraceFileName = ""
    _appTraceFile = ""
    _appDataFileName = "MarksIpDetectAndNotify061525_data.json"
    _appDataFile = ""
    _appSettingsFileName = "appsettings.json"
    _appSettingsFile = ""

    # JSON-able dict object.
    _currentAppData = {
        "_currentIpAddress": "",
        "_lastUpdatedDateTimeFormatted":""
    }

    def Init(self):
        self._currentDateTime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")        
        self._currentComputerName = socket.gethostname()       
        self._currentFilePath = __file__
        self._currentDirectory = os.path.dirname (self._currentFilePath)
        self._currentFileNameNoExt = FileU.GetFilenameWithoutExtension (self._currentFilePath)
        self._appDataFileName = f"{self._currentFileNameNoExt}_data.json"
        self._appTraceFileName = f"{self._currentFileNameNoExt}_trc.txt"
        self._appDataFile = os.path.join (self._currentDirectory, self._appDataFileName)
        self._appTraceFile = os.path.join (self._currentDirectory, self._appTraceFileName)
        self._appSettingsFile = os.path.join (self._currentDirectory, self._appSettingsFileName)

class AppSettings:
    senderAddress = ""
    loginText = ""
    recipAddress = ""


g_AppEnv = AppEnv()
g_AppEnv.Init()
TraceU.g_bTrcToFile = True ;

TraceU.g_sTrcFile = g_AppEnv._appTraceFile ;


################
# Send email via google
# ref: 
# https://mailtrap.io/blog/python-send-email-gmail/
# 
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

###########################################################
#Main program start


TraceU.trc ("***************************************") ;
TraceU.trc ("Program starting " + TraceU.sGetPN()) ;

log = f"App Data File is {g_AppEnv._appDataFile}"
TraceU.trc (log)

log = f"Tracing to {g_AppEnv._appTraceFile}"
TraceU.trc (log)

log = f"Loading App Settings File {g_AppEnv._appSettingsFile}"
TraceU.trc (log)
appSettingsJson = FileU.ReadFileIntoString (g_AppEnv._appSettingsFile)
if (BufU.StrIsEmpty(appSettingsJson)):
    log = f"Error Loading App Settings File {g_AppEnv._appSettingsFile}"
    sys.exit (-1)

appSettings = json.loads (appSettingsJson)  
senderAddress = appSettings['senderAddress'] 
loginText = appSettings['loginText']
recipAddress = appSettings['recipAddress']

if (BufU.StrIsEmpty(loginText)):
    log = f"loginText not set in App Settings File {g_AppEnv._appSettingsFile}"
    sys.exit (-1)
if (BufU.StrIsEmpty(senderAddress)):
    log = f"senderAddress not set in App Settings File {g_AppEnv._appSettingsFile}"
    sys.exit (-1)
if (BufU.StrIsEmpty(recipAddress)):
    log = f"recipAddress not set in App Settings File {g_AppEnv._appSettingsFile}"
    sys.exit (-1)


# https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
# https://www.ipify.org/
ip = get('https://api.ipify.org').text
# print(f"Public IP address for {g_AppEnv._currentComputerName} is: {ip}")
log = f"Public IP address for {g_AppEnv._currentComputerName} is: {ip}"
TraceU.trc (log)

g_AppEnv._currentAppData["_currentIpAddress"] = ip ; 
g_AppEnv._currentAppData["_lastUpdatedDateTimeFormatted"] = DateTimeU.GetCurrentDateTimeFormatted() ; 

currentAppDataJson = json.dumps (g_AppEnv._currentAppData)
g_CurrentAppData = json.loads (currentAppDataJson)

ipChanged = False 
lastSaveAppData = None
lastSavedAppDataJson = FileU.ReadFileIntoString (g_AppEnv._appDataFile)
if (not BufU.StrIsEmpty(lastSavedAppDataJson)):
    lastSaveAppData = json.loads(lastSavedAppDataJson)

    lastIp = lastSaveAppData["_currentIpAddress"]

    if (not BufU.StrIsEmpty(lastIp) and lastIp != ip):
        ipChanged = True
else:
    ipChanged = True

if (ipChanged):

    subject = f"IP Update {g_AppEnv._currentAppData["_lastUpdatedDateTimeFormatted"]}"
    body = "Current IP is " + ip
    body += "\n"
    body += f"Sent from {g_AppEnv._currentComputerName}"
    recipients = [recipAddress]

    log = f"Sending email notification to {recipAddress} subject {subject}"
    TraceU.trc (log)

    send_email(subject, body, senderAddress, recipients, loginText)

    FileU.WriteStringToFile (g_AppEnv._appDataFile, currentAppDataJson)

else:
    log = f"IP address did not change from {ip}" 
    TraceU.trc (log)


TraceU.trc ("Program exiting " + TraceU.sGetPN()) ;
