from settings.storage_handler import StorageHandler
from datetime import datetime
import tradfri.tradfri_handler as tradfri_handler
from threading import Timer
import logs
import time

timer = None
storageHandler = StorageHandler()

#ANCHOR starters
def start():
    storageHandler.addStorageUpdateListener(rescheduleNextEvent)
    scheduleNextEvent()

def performEventAndScheduleNext(event):
    performEvent(event)
    scheduleNextEvent()

def rescheduleNextEvent():
    if timer is None: return
    timer.cancel()
    scheduleNextEvent()


def scheduleNextEvent():
    global timer
    event = findNextEvent()
    eventTime = event["timeInMin"]
    nowInMin = getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 60*24
    eventTimeFromNow = eventTime + day - nowInMin
    logs.log("scheduleding for:", event, "(\"timeInMin\" is including a day if the event is tomorrow), in ", eventTimeFromNow, " miniutes")

    timer = Timer(eventTimeFromNow * 60, lambda: performEventAndScheduleNext(event))
    timer.start()


def findNextEvent():
    curNearestEvent = None
    events = storageHandler.getStorageContentCopy()["routined"]["events"]
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


def performEvent(event):
    for device in storageHandler.getStorageContentCopy()["routined"]["lamps"]:
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



