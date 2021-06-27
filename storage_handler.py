import json
from genericpath import isfile
import storage_items

FILE_NAME = "storage.json"

storageContent = None
storageContentUpdateListeners = []

def getStorageContent():
    return storageContent
    

def saveInputStorageContent(input):
    global storageContent

    storageContent = input
    with open(FILE_NAME, "w") as filestream:
        json.dump(storageContent, filestream)

    callOnUpdateListeners()
    

def callOnUpdateListeners():
    for listener in storageContentUpdateListeners:
        listener()


def readInStorageContent():
    global storageContent

    if(not isfile(FILE_NAME)):
        storageContent = storage_items.getNewStorageItem()
        return

    with open(FILE_NAME, "r") as fileStream:
        storageContent = json.load(fileStream)

    callOnUpdateListeners()
    


def setup():
    readInStorageContent()

setup()