import os
import TraceU

def GetFilenameWithoutExtension(path):
  """
  Extracts the filename without the extension from a given path.

  Args:
    path: The file path.

  Returns:
    The filename without the extension.
  """
  filename = os.path.basename(path)
  name_without_extension = os.path.splitext(filename)[0]

  return name_without_extension

def GetFileExtension(path):
  """
  Extracts the filename without the extension from a given path.

  Args:
    path: The file path.

  Returns:
    The filename without the extension.
  """

  fn = "GetFileExtension()"
  file_extension = ""

  try:
    filename = os.path.basename(path)
    file_extension = os.path.splitext(filename)[1]
  except Exception as e:
    # Code to handle any exception
    TraceU.trc(f"{fn} An error occurred: {e}")

  return file_extension

##########
#
def ReadFileIntoString (filePath):
    
    file_content = ""

    fileExists = os.path.exists (filePath)
    if (not fileExists):
        return file_content

    with open(filePath, 'r') as file:
        file_content = file.read()
        return file_content

#####
#
def WriteStringToFile (filePath, stringToWrite):
    
    file = open(filePath, "w")
    file.write(stringToWrite)
    file.close()

#################################
#
def bFileExists (sFilePath):
    br = os.path.isfile(sFilePath) ;
    return br ;
#################################
#
def DeleteFile (sFilePath):
    
    b = bFileExists (sFilePath) ;
    if (not b):
        return None ;
    
    #http://stackoverflow.com/questions/1995373/deleting-files-in-python
    os.remove(sFilePath) ;
    
    return None ;
#################################
#
def iGetFileSize (sFilePath):
    ir = -1 ;
    
    b = bFileExists (sFilePath) ;
    if (not b):
        return ir ;
    
    
    #http://stackoverflow.com/questions/6591931/getting-file-size-in-python
    ir = os.stat(sFilePath).st_size 
    
    return ir ;
#################################
#
def AppendTextToFile (sFilePath, sText):
    
    trcFile =  None;
    try:
        trcFile = open(sFilePath, "a");
        trcFile.write(sText) ;
        #trcFile.close() ;
        #trcFile = None ;
    except:
        sError = "Error writing to trace file " + sFilePath ;
        TraceU.trcError(sError) ;
        
    if (trcFile != None):
        trcFile.close ;
        trcFile = None ;
                
    return None ;