from settings.storage_handler import StorageHandler
import tradfri.tradfri_handler as tradfri_handler
import json
import logs
import subprocess
import sys


def getSettings(_):
    storageContentJson = json.dumps(StorageHandler().getStorageContentCopy())
    return dict(resCode = 200, mimeType="text/json", fileContent=storageContentJson.encode('utf-8'))

def lampPickerJson(_):
    contentDict = dict(devices = tradfri_handler.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def deviceControlJson(query):
    deviceId = json.loads(query["device"][0])["id"]
    action = query["action"][0]
    payload = query["payload"][0]

    tradfri_handler.performAction(deviceId, action, payload)

    contentDictStr = "d:a"
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def logJson(_):
    logsList = logs.getLogs()
    logsJson = json.dumps(logsList)
    return dict(resCode = 200, mimeType="text/json", fileContent=logsJson.encode('utf-8'))

def doUpdate(_):
    subprocess.Popen("bash_scripts/update.sh")
    sys.exit()



specialRoutes = {
    "settings":getSettings,
    "lampPickerJson":lampPickerJson,
    "deviceControlJson":deviceControlJson,
    "logJson":logJson,
    "doUpdate":doUpdate
}


def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName

def getspecialRouteFileDict(location, query):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute(query)
    return newLocation

