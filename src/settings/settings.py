import json
import os
import logger

class Settings:
    FILE_PATH = "settings/settings.json"
    endpoint = None
    gatewayAddr = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
            cls.instance.loadSettings()
        return cls.instance


    def loadSettings(self):
        if(not os.path.isfile(self.FILE_PATH)):
            logger.log("no settings file")
            quit()

        with open(self.FILE_PATH, "r") as f:
            settings = json.load(f)
            print(settings, flush=1)
            self.endpoint = settings["endpoint"]
            self.gatewayAddr = settings["gatewayAddr"]