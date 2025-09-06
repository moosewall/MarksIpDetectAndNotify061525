import sys
import datetime

import FileU

g_bTrcToFile = False ;
g_sTrcFile = "" ;
g_iTrcFileMax = 5000000 ; #Max trace file size before reset
#g_iTrcFileMax = 100 ; #Max trace file size before reset, quick test

########################
#Get program name
#
"""
refs 
http://doughellmann.com/2012/04/determining-the-name-of-a-process-from-python-2.html
"""
#
def sGetPN ():
   
    sr =  sys.argv[0] ;
    
    return sr ;
########################
#
def sGetFN ():
    
    #http://code.activestate.com/recipes/66062-determining-current-function-name/
    sr = sys._getframe(1).f_code.co_name + "()" ;
    
    return sr ;
#########################
#
def sFormatTrc (sTrc):
    
    #http://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component
    #sDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ;
    sDateTime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S") ;
    
    sTrcWDateTime = sDateTime + " " + sTrc ;
    sTrcWEol = sTrcWDateTime + "\n" ;

    sr = sTrcWEol ;
    return sr
#########################
#
def trc (sTrc):
    
   
    sTrcFormatted = sFormatTrc (sTrc) ;
    
    trcToConsole (sTrcFormatted)
    trcToFile (sTrcFormatted)
    
    return None ;
######################################3
#
def trcError (sTrc):
    print (sTrc)
    return None ;
##########################
#
def trcToConsole (sTrc):
    
    print (sTrc) ;
    
    return None ;
##########################
#
def trcToFile (sTrc):
    
   
    if (    g_bTrcToFile != True
        or g_sTrcFile == ""):
        return None ;
    
    #///////////////////////////
    iTrcFileSz = FileU.iGetFileSize(g_sTrcFile) ;
    if (iTrcFileSz > g_iTrcFileMax):
        
        FileU.DeleteFile (g_sTrcFile) ;
        
        #wrong
        #sTrcDel = g_sTrcFile + " reset because size " + iTrcFileSz + " greater then max " + g_iTrcFileMax ;
        
        #http://stackoverflow.com/questions/1225637/python-string-formatting
        sTrcDel = "{0} reset because size {1} greater than max {2}".format \
            (g_sTrcFile, \
             iTrcFileSz, \
             g_iTrcFileMax) ;      
        
        sTrcDel = sFormatTrc (sTrcDel)
        FileU.AppendTextToFile (g_sTrcFile, sTrcDel) ;
    #///////////////////////////    
    
    FileU.AppendTextToFile (g_sTrcFile, sTrc) ;
    
    return None ;