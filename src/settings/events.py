import json
from genericpath import isfile
import math
from . import storage_items
import logger
import copy

class Events:
    events = []


    #========== CONSTRUCTOR ==========

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Events, cls).__new__(cls)
            cls.instance.loadSettings()
        return cls.instance


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

