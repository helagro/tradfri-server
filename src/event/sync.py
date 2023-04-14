import schedule
from event.events import Events
from settings.settings import Settings
import requests
import traceback
import time
import logger


def scheduleSync():
    schedule.every().day.at("04:00").do(sync)
    while True: 
        time.sleep(50*60)
        schedule.run_pending()


def sync():
    logger.log("syncing...")

    syncData = getRoutinesSyncData()

    if not syncData is None:
        Events().setEvents(syncData)


def getRoutinesSyncData():
    endpoint = Settings().endpoint
    params = {
        "command": "tradfri"
    }
    
    if endpoint is None: 
        logger.log("won't sync, syncing endpoint is not defined")
        return

    try:
        response = requests.get(endpoint, params=params, timeout=60)  
        jsonResponse = response.json()
        
        logger.log("successful sync")
        return jsonResponse
    except:
        logger.log("sync failed", traceback.format_exc())