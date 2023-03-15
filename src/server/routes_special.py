from settings.events import StorageHandler
from tradfri.tradfri_interface import TradfriInterface
import json
import logger
import subprocess
import sys
from .my_mime_types import MyMimeTypes
import events
from .my_response_successful import MyResponseSuccessful

tradfriInterface = TradfriInterface()



#========== SPECIFIC ROUTES ==========

def getSettings(_):
    storageContentJson = json.dumps(StorageHandler().getStorageContentCopy())
    return MyResponseSuccessful(MyMimeTypes.JSON, storageContentJson.encode('utf-8'))

def getDevices(_):
    contentDict = dict(devices = tradfriInterface.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def performAction(query: dict):
    deviceId = json.loads(query["device"][0])["id"]
    action = query["action"][0]
    payload = query["payload"][0] if "payload" in query else None
    result = None

    if(action == "performEvent"):
        events.performEventByName(payload)
        result = {"success": True}
    else:
        result = tradfriInterface.performAction(deviceId, action, payload)
        
    contentDictStr = None if result == None else json.dumps(result)
    fileContent = contentDictStr.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def getColor(query):
    deviceId = json.loads(query["device"][0])["id"]

    deviceStatus = tradfriInterface.getDeviceStatus(deviceId)

    fileContent = deviceStatus.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def getLogs(_):
    logsList = logger.getLogs()
    logsJson = json.dumps(logsList)
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent=logsJson.encode('utf-8'))

def doUpdate(_):
    subprocess.Popen("bash_scripts/update.sh")
    sys.exit()


specialRoutes = {
    "settings":getSettings,
    "lampPickerJson":getDevices,
    "deviceControlJson":performAction,
    "logJson":getLogs,
    "doUpdate":doUpdate
}


#========== GENERAL METHODS ==========

def hasRoute(location):
    routeMethod = getRoute(location)
    return not (routeMethod is None)

def getspecialRouteFileDict(location, query):
    routeMethod = getRoute(location)

    if(routeMethod is None): return

    result = routeMethod(query)
    return result

def getRoute(location):
    routeString = locationToRouteString(location)
    return specialRoutes.get(routeString, None)

def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName

