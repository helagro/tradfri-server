import schedule
from event.events import Events
from settings.settings import Settings
import requests
import traceback
import time
import logger


def scheduleSync() -> None:
    schedule.every().day.at("04:00").do(_sync)
    while True: 
        time.sleep(50*60)
        schedule.run_pending()


def sync() -> None:
    logger.log("syncing...")

    syncData = _getRoutinesSyncData()

    if not syncData is None:
        Events().setEvents(syncData)


def _getRoutinesSyncData():
    endpoint = Settings().getEndpoint()
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
        logger.log("sync failed: ", traceback.format_exc())