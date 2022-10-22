from ast import Num
from settings.storage_handler import StorageHandler
from datetime import datetime
from . import tradfri_handler
from threading import Timer
import logs
import time

timer = None
STORAGE_HANDLER = StorageHandler()


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


#========== PERFORM EVENT ==========

def performEvent(event):
    for device in event["lamps"]:
        try:
            performEventForDevice(event, device)
        except Exception as e:
            logs.log("Performing scheduled event failed because: ", e)
    logs.log("performed timed event: " + event["name"])

def performEventForDevice(event, device):
    isOn = tradfri_handler.performAction(device, "isOn", None)
    tradfri_handler.performAction(device, "setBrightness", event["brightness"])
    time.sleep(3)
    tradfri_handler.performAction(device, "setColor", event["color"])
    time.sleep(3)
    tradfri_handler.performAction(device, "setState", isOn)



