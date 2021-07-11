import storage_handler
from datetime import datetime
import tradfri_handler
import time
import logs



def preformEvent(event):
    for device in storage_handler.getStorageContent()["routined"]["lamps"]:
        isOn = tradfri_handler.performAction(device, "isOn", None)
        tradfri_handler.performAction(device, "setColor", event["color"])
        tradfri_handler.performAction(device, "setBrightness", event["brightness"])
        tradfri_handler.performAction(device, "setState", isOn)
    logs.addLog("performed timed event: " + event["name"])


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

def addRelevantDaysToEvents(event):
    currentTime = getCurTimeInMin()

    if(event["timeInMin"] < currentTime):
        event["timeInMin"] += (24*60 - currentTime)




def findNextEvent():
    curNearestEvent = None
    events = storage_handler.getStorageContent()["routined"]["events"]
    for event in events:
        addRelevantDaysToEvents(event)

        if(curNearestEvent is None or (event["timeInMin"] < curNearestEvent["timeInMin"])):
            curNearestEvent = event

    return curNearestEvent


def start():
    nextEvent = findNextEvent()
    logs.addLog("scheduleding for:", nextEvent, "(Time in minute is delay, not from 0:00!!)")
    scheduleEvent(nextEvent)


