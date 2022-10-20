from settings.storage_handler import StorageHandler
import tradfri.tradfri_handler as tradfri_handler
import json
import logs
import subprocess
import sys
from my_response_successful import MyResponseSuccessful


#========== SPECIFIC ROUTES ==========

def getSettings(_):
    storageContentJson = json.dumps(StorageHandler().getStorageContentCopy())
    return MyResponseSuccessful("text/json", storageContentJson.encode('utf-8'))

def getDevices(_):
    contentDict = dict(devices = tradfri_handler.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return MyResponseSuccessful("text/json", fileContent=fileContent)

def getDeviceInfo(query):
    deviceId = json.loads(query["device"][0])["id"]
    action = query["action"][0]
    payload = query["payload"][0]

    result = tradfri_handler.performAction(deviceId, action, payload)
    contentDictStr = "d:a" if result == None else json.dumps(result)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def getColor(query):
    deviceId = json.loads(query["device"][0])["id"]

    deviceStatus = tradfri_handler.getDeviceStatus(deviceId)

    fileContent = deviceStatus.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)


def getLogs(_):
    logsList = logs.getLogs()
    logsJson = json.dumps(logsList)
    return dict(resCode = 200, mimeType="text/json", fileContent=logsJson.encode('utf-8'))

def doUpdate(_):
    subprocess.Popen("bash_scripts/update.sh")
    sys.exit()

specialRoutes = {
    "settings":getSettings,
    "lampPickerJson":getDevices,
    "deviceControlJson":getDeviceInfo,
    "logJson":getLogs,
    "doUpdate":doUpdate
}


#========== GENERAL METHODS ==========



def hasRoute(location):
    routeString = locationToRouteString(location)
    matchingRoute = specialRoutes.get(routeString, None)
    return not (matchingRoute is None)

def getspecialRouteFileDict(location, query):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute(query)
    return newLocation

def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName

