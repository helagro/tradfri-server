from genericpath import isfile
import json
import logger

class Settings:
    FILE_PATH = "settings/storage.json"
    endpoint = None
    gatewayAddr = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
            cls.instance.loadSettings()
        return cls.instance


    def loadSettings(self):
        if(not isfile(self.FILE_PATH)):
            logger.log("no storage file")
            quit()

        with open(self.FILE_PATH, "r") as f:
            settings = json.loads(f)
            self.endpoint = settings["endpoint"]
            self.gatewayAddr = settings["gatewayAddr"]
            self.storageContent = json.load(f)