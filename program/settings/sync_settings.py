from settings.storage_handler import StorageHandler
import requests
import logs

def sync():
    routines = getRoutinesToSync()
    logs.log("Routines to sync", routines)
    syncRoutines(routines)

def getRoutinesToSync():
    routinesToSync = []
    for routine in StorageHandler().storageContent["events"]:
        if("isSynced" in routine and routine["isSynced"] == True):
            routinesToSync.append(routine)
    return routinesToSync

def syncRoutines(routines):
    storageHandler = StorageHandler()
    endpoint = storageHandler.getSyncEndpoint()
    if(endpoint is None): 
        logs.log("Won't sync, syncing endpoint is not defined")
        return

    for routine in routines:
        syncRoutine(routine, endpoint)

def syncRoutine(routine, endpoint):
    response = requests.post(endpoint, routine["name"])
    logs.log(f"Sent syncing post request for {routine['name']} to {endpoint}. Response was {response.content}")
