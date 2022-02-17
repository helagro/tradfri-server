import settings.storage_handler as storage_handler
import tradfri.tradfri_handler as tradfri_handler
import json
import logs
import subprocess
import sys


def allSafeStorageParameters(query):
    storageContentJson = json.dumps(storage_handler.getStorageContentCopy())
    return dict(resCode = 200, mimeType="text/json", fileContent=storageContentJson.encode('utf-8'))

def lampPickerJson(query):
    contentDict = dict(devices = tradfri_handler.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def deviceControlJson(query):
    deviceId = json.loads(query["device"][0])["id"]
    action = query["action"][0]
    payload = query["payload"][0]
    logs.log("deviceId", deviceId, "action", action, "payload", payload)

    tradfri_handler.performAction(deviceId, action, payload)

    contentDictStr = "d:a"
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def logJson(query):
    logsList = logs.getLogs()
    logsJson = json.dumps(logsList)
    return dict(resCode = 200, mimeType="text/json", fileContent=logsJson.encode('utf-8'))

def doUpdate(query):
    subprocess.Popen("bash_scripts/update.sh")
    sys.exit()



specialRoutes = {
    "allSafeStorageParameters":allSafeStorageParameters,
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

