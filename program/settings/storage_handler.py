import json
from genericpath import isfile
from . import storage_items
import logs
import copy

class StorageHandler:
    FILE_NAME = "settings/storage.json"

    storageContent = None
    storageContentUpdateListeners = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StorageHandler, cls).__new__(cls)
            cls.instance.loadSettings()
        return cls.instance


    def loadSettings(self):
        if(not isfile(self.FILE_NAME)):
            self.storageContent = storage_items.getNewStorageItem()
            logs.log("no storage file")
            return

        with open(self.FILE_NAME, "r") as fileStream:
            self.storageContent = json.load(fileStream)

        self.callOnUpdateListeners()

    def calculateTimeInMin(self, storageContent) -> None:
        events = storageContent["events"]

        for event in events:
            timeStr = event["timeStr"]
            timeStrSplit = timeStr.split(":")
            hour = timeStrSplit[0]
            min = timeStrSplit[1]
            event["timeInMin"] = int(hour) * 60 + int(min)

    def saveInputStorageContent(self, input):
        self.storageContent = input
        with open(self.FILE_NAME, "w") as filestream:
            json.dump(self.storageContent, filestream)

        self.callOnUpdateListeners()


    #========== LISTENERS ==========

    def addStorageUpdateListener(self, storageUpdateListener):
        self.storageContentUpdateListeners.append(storageUpdateListener)

    def callOnUpdateListeners(self):
        for listener in self.storageContentUpdateListeners:
            listener()


    #========== OTHER ==========

    def getStorageContentCopy(self):
        return copy.deepcopy(self.storageContent)



        



        