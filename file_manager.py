from genericpath import isfile
from urllib import parse
import os

FILE_FOLDER = "public"


def getFilePath(fileName):
    if(fileName == "/"):
        fileName = os.sep + "index.html"

    return FILE_FOLDER + fileName


def getMimeType(filePath):
    fileExtension = os.path.splitext(filePath)[1]

    vaildMimeTypes = {
        ".html" : "text/html",
        ".css" : "text/css",
    }
    return vaildMimeTypes.get(fileExtension, None)



def getFile(fileName):
    filePath = getFilePath(fileName)
    mimeType = getMimeType(filePath)

    if(not isfile(filePath)):
        return getFile("/404.html")

    if(mimeType is None):
        return dict(resCode=501)

    fileStream = open(filePath, "rb")
    fileContent = fileStream.read()
    fileStream.close()
    
    return dict(resCode=200, mimeType=mimeType, fileContent=fileContent)