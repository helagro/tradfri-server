import json
from genericpath import isfile
import storage_items
import copy

FILE_NAME = "storage.json"

storageContent = None


def clearFeildsIn(object, property):
    dictionary = object[property]

    for key in dictionary:
        dictionary[key] = "**********"


def getSafeStorageContentJson():
    storageContentCopy = copy.deepcopy(storageContent)
    clearFeildsIn(storageContentCopy, "private")
    safeJson = json.dumps(storageContentCopy)
    return safeJson
    

def saveInputStorageContent(input):
    global storageContent

    privateDict = input["private"]

    for key in privateDict:
        if(privateDict[key] == "**********"):
            privateDict[key] = privateDict[key]

    storageContent = input
    with open(FILE_NAME, "w") as filestream:
        json.dump(storageContent, filestream)


def readInStorageContent():
    global storageContent

    if(not isfile(FILE_NAME)):
        storageContent = storage_items.getNewStorageItem()
        return

    with open(FILE_NAME, "r") as fileStream:
        storageContent = json.load(fileStream)


def setup():
    readInStorageContent()

setup()