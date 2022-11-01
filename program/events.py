from ast import Num
from settings.storage_handler import StorageHandler
from datetime import datetime
from threading import Timer
import logs
import time
from tradfri.tradfri_interface import TradfriInterface

timer = None
STORAGE_HANDLER = StorageHandler()
TRADFRI_INTERFACE = TradfriInterface()


#========== ENTRY POINTS ==========

def start():
    STORAGE_HANDLER.addStorageUpdateListener(rescheduleEvent)
    scheduleNextEvent()


def performEventAndScheduleNext(event):
    performEvent(event)
    scheduleNextEvent()


def rescheduleEvent():
    if timer is None: return
    timer.cancel()
    scheduleNextEvent()

def performEventByName(eventName: str):
    event = findEvent(eventName)
    performEvent(event)


#========== SCHEDULING ROUTINE ==========

def scheduleNextEvent():
    event = findNextEvent()
    minutesToNextEvent = getMinutesToNextEvent(event)
    
    logs.log("scheduleding for:", event, "(\"timeInMin\" is including a day if the event is tomorrow), in ", minutesToNextEvent, " miniutes")
    scheduleEvent(event, minutesToNextEvent)


def findNextEvent():
    curNearestEvent = None
    events = STORAGE_HANDLER.getStorageContentCopy()["events"]
    for event in events:
        event["timeInMin"] = addRelevantDaysToEvent(event)

        if(curNearestEvent is None or (event["timeInMin"] < curNearestEvent["timeInMin"])):
            curNearestEvent = event

    return curNearestEvent


def addRelevantDaysToEvent(event):
    currentTime = getCurTimeInMin()

    if(event["timeInMin"] <= currentTime):
        return event["timeInMin"] + 24*60
    return event["timeInMin"]


def getCurTimeInMin():
    now = datetime.now()
    return now.hour * 60 + now.minute


def getMinutesToNextEvent(event):
    eventTime = event["timeInMin"]
    nowInMin = getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 60*24
    return eventTime + day - nowInMin


def scheduleEvent(event, minutesFromNow):
    global timer

    if not timer is None: timer.cancel()
    timer = Timer(minutesFromNow * 60, lambda: performEventAndScheduleNext(event))
    timer.start()


#========== OTHER ==========

def findEvent(eventName: str) -> dict:
    events = STORAGE_HANDLER.getStorageContentCopy()["events"]
    for event in events:
        if event["name"] == eventName:
            return event


#========== PERFORM EVENT ==========

def performEvent(event):
    for action in event["actions"]:
        try:
            TRADFRI_INTERFACE.performAction(action["device"], action["name"], action["payload"])
        except Exception as e:
            logs.log(f"Performing action: '{action}' in scheduled event: '{event}' failed because: ", e)

        time.sleep(3)
    logs.log("performed timed event: " + event["name"])