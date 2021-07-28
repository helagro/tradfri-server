import storage_handler
from datetime import datetime
import tradfri_handler
import time
import logs

def performEventForDevice(event, device):
    isOn = tradfri_handler.performAction(device, "isOn", None)
    tradfri_handler.performAction(device, "setBrightness", event["brightness"])
    time.sleep(3)
    tradfri_handler.performAction(device, "setColor", event["color"])
    time.sleep(3)
    tradfri_handler.performAction(device, "setState", isOn)

def preformEvent(event):
    for device in storage_handler.getStorageContentCopy()["routined"]["lamps"]:
        performEventForDevice(event, device)
    logs.log("performed timed event: " + event["name"])


def scheduleEvent(event):
    eventTime = event["timeInMin"]
    nowInMin = getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 60*24
    eventTimeFromNow = eventTime + day - nowInMin
    logs.log("scheduleding for:", event, "(Time in minute is including a day if the event is tomorrow), in ", eventTimeFromNow, " miniutes")

    time.sleep(eventTimeFromNow * 60)

    preformEvent(event)
    start()

def getCurTimeInMin():
    now = datetime.now()
    return now.hour * 60 + now.minute

def addRelevantDaysToEvent(event):
    currentTime = getCurTimeInMin()

    if(event["timeInMin"] <= currentTime):
        return event["timeInMin"] + 24*60
    return event["timeInMin"]




def findNextEvent():
    curNearestEvent = None
    events = storage_handler.getStorageContentCopy()["routined"]["events"]
    for event in events:
        event["timeInMin"] = addRelevantDaysToEvent(event)

        if(curNearestEvent is None or (event["timeInMin"] < curNearestEvent["timeInMin"])):
            curNearestEvent = event

    return curNearestEvent


def start():
    nextEvent = findNextEvent()
    scheduleEvent(nextEvent)


