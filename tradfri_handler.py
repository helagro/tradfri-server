import pytradfri
import storage_handler

gateway = pytradfri.Gateway()
isSetup = False


def setup():
    PRIVATE_STORAGE = storage_handler.getStorageContent()["private"]
    if(PRIVATE_STORAGE["gatewayUsername"] is None or PRIVATE_STORAGE["gatewayPresharedKey"] is None):
        isSetup = False
        return 

    isSetup = True
    

setup()
