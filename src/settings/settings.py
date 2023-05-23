import json
import os
import logger

class Settings:
    _FILE_PATH = "settings/settings.json"
    _endpoint = None
    _gatewayAddr = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self._loadSettings()



    def getEndpoint(self):
        return self._endpoint
    
    def getGatewayAddr(self):
        return self._gatewayAddr



    def _loadSettings(self):
        if(not os.path.isfile(self._FILE_PATH)):
            logger.log("no settings file")
            quit()

        with open(self._FILE_PATH, "r") as f:
            settings = json.load(f)
            logger.log(settings)
            self._endpoint = settings["endpoint"]
            self._gatewayAddr = settings["gatewayAddr"]