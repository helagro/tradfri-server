from settings.storage_handler import StorageHandler
import requests
import logs


def sync():
    syncData = getRoutinesSyncData()
    if syncData is None: return
    logs.log(f"data from sync: {syncData}")
    updateEventsValues(syncData)


def getRoutinesSyncData():
    storageHandler = StorageHandler()
    endpoint = storageHandler.getSyncEndpoint()
    if endpoint is None: 
        logs.log("Won't sync, syncing endpoint is not defined")
        return

    response = requests.get(endpoint)
    try:
        responseJson = response.json()
        return responseJson["result"]
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
                break
        else:
            logs.log(f"event '{name}' exists in the sync but not locally")

    storageHandler.saveInputStorageContent(storageHandler.storageContent)


def updateEventValues(event, timeInMin):
    event["timeInMin"] = timeInMin
    event["timeStr"] = StorageHandler().calculateTimeStr(timeInMin)