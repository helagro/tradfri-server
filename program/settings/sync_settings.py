from settings.storage_handler import StorageHandler
import requests
import logs


def sync():
    logs.log("Starting sync...")
    syncData = getRoutinesSyncData()
    if syncData is None: return
    logs.log(f"data from sync: {syncData}")
    updateEventsValues(syncData)


def getRoutinesSyncData():
    storageHandler = StorageHandler()
    endpoint = storageHandler.getSyncEndpoint()
    params = {
        "command": "tradfri"
    }
    if endpoint is None: 
        logs.log("Won't sync, syncing endpoint is not defined")
        return

    try:
        response = requests.get(endpoint, params=params, timeout=60)  
        responseJson = response.json()
        return responseJson["result"]
    except:
        logs.log(f"sync failed: {response}")


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
                break
        else:
            logs.log(f"event '{name}' exists in the sync but not locally")

    storageHandler.saveInputStorageContent(storageHandler.storageContent)


def updateEventValues(event, timeInMin):
    event["timeInMin"] = timeInMin
    event["timeStr"] = StorageHandler().calculateTimeStr(timeInMin)