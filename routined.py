import storage_handler
from datetime import datetime
import tradfri_handler
import time
import logs



def preformEvent(event):
    for device in storage_handler.getStorageContentCopy()["routined"]["lamps"]:
        isOn = tradfri_handler.performAction(device, "isOn", None)
        tradfri_handler.performAction(device, "setColor", event["color"])
        tradfri_handler.performAction(device, "setBrightness", event["brightness"])
        tradfri_handler.performAction(device, "setState", isOn)
    logs.log("performed timed event: " + event["name"])


def scheduleEvent(event):
    eventTime = event["timeInMin"]
    nowInMin = getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 60*24
    eventTimeFromNow = eventTime + day - nowInMin

    time.sleep(eventTimeFromNow * 60)

    preformEvent(event)
    start()

def getCurTimeInMin():
    now = datetime.now()
    return now.hour * 60 + now.minute

def addRelevantDaysToEvent(event):
    currentTime = getCurTimeInMin()

    if(event["timeInMin"] < currentTime):
        return event["timeInMin"] + 24*60
    return event["timeInMin"]




def findNextEvent():
    curNearestEvent = None
    events = storage_handler.getStorageContentCopy()["routined"]["events"]
    for event in events:
        event["timeInMin"] = addRelevantDaysToEvent(event)

        print("hi", event, curNearestEvent)

        if(curNearestEvent is None or (event["timeInMin"] < curNearestEvent["timeInMin"])):
            curNearestEvent = event

    return curNearestEvent


def start():
    nextEvent = findNextEvent()
    logs.log("scheduleding for:", nextEvent, "(Time in minute is including a day if the event is tomorrow)")
    scheduleEvent(nextEvent)


