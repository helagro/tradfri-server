import math
from settings.storage_handler import StorageHandler
import requests
import logs

def sync():
    syncData = getRoutinesSyncData()
    if syncData is None: return
    logs.log(f"syncData: {syncData}")
    updateEventsValues(syncData['result'])


def getRoutinesSyncData():
    storageHandler = StorageHandler()
    endpoint = storageHandler.getSyncEndpoint()
    if endpoint is None: 
        logs.log("Won't sync, syncing endpoint is not defined")
        return

    response = requests.get(endpoint)
    try:
        return response.json()
    except:
        logs.log(f"Invalid sync data: {response}")
        


def updateEventsValues(syncData):
    storageHandler = StorageHandler()
    events = storageHandler.storageContent["events"]
    for syncDataValues in syncData:
        name = syncDataValues["name"]
        timeValue = syncDataValues["time"]
        timeInMin = storageHandler.calculateTimeInMin(timeValue, ".")

        for event in events:
            if event["name"] == name:
                updateEventValues(event, timeInMin)

    storageHandler.saveInputStorageContent(storageHandler.storageContent)

def updateEventValues(event, timeInMin):
    event["timeInMin"] = timeInMin
    minutes = timeInMin % 60
    hours = math.floor(timeInMin / 60)
    minutesStr = format(minutes, '02d')
    event["timeStr"] = f"{hours}:{minutesStr}"