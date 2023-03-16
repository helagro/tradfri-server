from settings.events import Events
from datetime import datetime
from threading import Timer
import logger
import time
from tradfri.tradfri_interface import TradfriInterface

timer = None
events = Events()
storageInterface = TradfriInterface()


#========== ENTRY POINTS ==========

def start():
    events.addStorageUpdateListener(rescheduleEvent)
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
    if event is None:
        logger.log("nothing to schedule, no events")
        return

    minutesToNextEvent = getMinutesToNextEvent(event)
    
    logger.log("scheduleding for:", event, "(\"timeInMin\" is including a day if the event is tomorrow), in ", minutesToNextEvent, " miniutes")
    scheduleEvent(event, minutesToNextEvent)


def findNextEvent():
    curNearestEvent = None
    for event in events.events:
        eventTime = addRelevantDaysToEvent(event)

        if(curNearestEvent is None or (eventTime < curNearestEvent["time"])):
            curNearestEvent = event

    return curNearestEvent


def addRelevantDaysToEvent(event):
    currentTime = getCurTimeInMin()

    if(event["time"] <= currentTime):
        return event["time"] + 24*60
    return event["time"]


def getCurTimeInMin():
    now = datetime.now()
    return now.hour * 60 + now.minute


def getMinutesToNextEvent(event):
    eventTime = event["time"]
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
    events = events.getStorageContentCopy()["events"]
    for event in events:
        if event["name"] == eventName:
            return event


#========== PERFORM EVENT ==========

def performEvent(event):
    for action in event["actions"]:
        try:
            storageInterface.commandRouter(action["device"], action["name"], action["payload"])
        except Exception as e:
            logger.log(f"Performing action: '{action}' in scheduled event: '{event}' failed because: ", e)

        time.sleep(3)
    logger.log("performed timed event: " + event["name"])