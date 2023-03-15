from settings.events import StorageHandler
from tradfri.tradfri_interface import TradfriInterface
import json
import logger
import subprocess
import sys
from .my_mime_types import MyMimeTypes
import schedule
from .my_response_successful import MyResponseSuccessful

tradfriInterface = TradfriInterface()


def route(location: dict):
    command = location["c"][0]

    if(command == "devices"): return getDevices()
    if(command == "logs"): return getLogs()
    if(command == "update"): return update()

    device = location["d"][0]
    payload = location["p"][0] if "p" in location else None

    performAction()

#========== SPECIFIC ROUTES ==========

def getDevices():
    contentDict = dict(devices = tradfriInterface.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def performAction(command, device, payload):
    if(command == "doEvent"):
        schedule.performEventByName(payload)
        result = {"success": True}
    else:
        result = tradfriInterface.performAction(device, command, payload)
        
    contentDictStr = None if result == None else json.dumps(result)
    fileContent = contentDictStr.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def getColor(query):
    deviceId = json.loads(query["device"][0])["id"]

    deviceStatus = tradfriInterface.getDeviceStatus(deviceId)

    fileContent = deviceStatus.encode('utf-8')
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent)

def getLogs():
    logsList = logger.getLogs()
    logsJson = json.dumps(logsList)
    return MyResponseSuccessful(MyMimeTypes.JSON, fileContent=logsJson.encode('utf-8'))

def update(_):
    subprocess.Popen("bash_scripts/update.sh")
    sys.exit()
