import logger
import requests
from settings.settings import Settings
import traceback
from settings import options

class Events:
    events = []
    storageContentUpdateListeners = []


    #========== CONSTRUCTOR ==========

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Events, cls).__new__(cls)
            
            if not options.noDownload:
                cls.instance.downloadEvents()

        return cls.instance


    def downloadEvents(self):
        logger.log("syncing...")

        syncData = self.getRoutinesSyncData()

        if not syncData is None:
            self.events = syncData


    def getRoutinesSyncData(self):
        endpoint = Settings().endpoint
        params = {
            "command": "tradfri"
        }
        
        if endpoint is None: 
            logger.log("won't sync, syncing endpoint is not defined")
            return

        try:
            response = requests.get(endpoint, params=params, timeout=60)  
            jsonResponse = response.json()
            
            logger.log("successful sync")
            return jsonResponse
        except:
            logger.log("sync failed", traceback.format_exc())


    #========== LISTENERS ==========

    def addStorageUpdateListener(self, storageUpdateListener):
        self.storageContentUpdateListeners.append(storageUpdateListener)

    def callOnUpdateListeners(self):
        for listener in self.storageContentUpdateListeners:
            listener()

