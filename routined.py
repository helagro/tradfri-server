import storage_handler
from datetime import datetime
import tradfri_handler
import time


def preformEvent(event):
    tradfri_handler.performAction(event["device"], "setColor", event["color"])
    tradfri_handler.performAction(event["device"], "setBrightness", event["brightness"])
    print("performed timed event: " + event["name"])


def scheduleEvent(event):
    eventTime = event["timeInMin"]
    nowInMin = getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 60*24
    eventTimeFromNow = eventTime + day - nowInMin

    time.sleep(eventTimeFromNow * 60)

    preformEvent(event)
    start()


def getCurTimeInMin():
    return datetime.hour * 60 + datetime.min


def findNextEvent():
    curTime = getCurTimeInMin()

    curNearestEvent = None
    events = storage_handler.getStorageContent()["routined"]["events"]
    for event in events:
        if((curNearestEvent is None) or ((event["timeInMin"] < curNearestEvent["timeInMin"]) and (event["timeInMin"] > curTime))):
            curNearestEvent = event

    return curNearestEvent


def start():
    print("routined started")

    nextEvent = findNextEvent()
    scheduleEvent(nextEvent)


