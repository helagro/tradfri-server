import logger
import requests
from .settings import Settings

class Events:
    events = []
    storageContentUpdateListeners = []


    #========== CONSTRUCTOR ==========

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Events, cls).__new__(cls)
            cls.instance.downloadEvents()
        return cls.instance


    def downloadEvents(self):
        logger.log("starting sync...")

        syncData = self.getRoutinesSyncData()
        logger.log(f"data from sync: {syncData}")

        if not syncData is None:
            self.events = syncData


    def getRoutinesSyncData(self):
        endpoint = Settings().endpoint
        params = {
            "command": "tradfri"
        }
        if endpoint is None: 
            logger.log("Won't sync, syncing endpoint is not defined")
            return

        try:
            response = requests.get(endpoint, params=params, timeout=60)  
            return response.json()
        except:
            logger.log(f"sync failed: {response}")

    #========== LISTENERS ==========

    def addStorageUpdateListener(self, storageUpdateListener):
        self.storageContentUpdateListeners.append(storageUpdateListener)

    def callOnUpdateListeners(self):
        for listener in self.storageContentUpdateListeners:
            listener()

