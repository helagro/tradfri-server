from genericpath import isfile
import os
from my_response import MyResponse
from my_response_successful import MyResponseSuccessful
from my_mime_types import MyMimeTypes

FILE_FOLDER = "public"


def getFile(fileName):
    filePath = getFilePath(fileName)
    mimeType = getMimeType(filePath)

    if(not isfile(filePath)):
        if(mimeType == MyMimeTypes.HTML):
            return getFile("/404.html")
        else:
            return MyResponse(404)

    fileStream = open(filePath, "rb")
    fileContent = fileStream.read()
    fileStream.close()
    
    return MyResponseSuccessful(mimeType, fileContent)


def getFilePath(fileName):
    if(fileName == "/"):
        fileName = os.sep + "index.html"

    return FILE_FOLDER + fileName


def getMimeType(filePath):
    fileExtension = os.path.splitext(filePath)[1]

    vaildMimeTypes = {
        ".html" : MyMimeTypes.HTML,
        ".css" : MyMimeTypes.CSS,
        ".js" : MyMimeTypes.JAVASCRIPT,
        ".json" : MyMimeTypes.JSON
    }
    return vaildMimeTypes.get(fileExtension, None)
