from settings.events import Events
from datetime import datetime
from threading import Timer
import logger
import time
from tradfri.tradfri_interface import TradfriInterface

timer = None
eventsHandler = Events()


#========== ENTRY POINTS ==========

def start():
    eventsHandler.addStorageUpdateListener(rescheduleEvent)
    scheduleNextEvent()


def performEventsAndScheduleNext(events):
    performEvents(events)
    scheduleNextEvent()


def rescheduleEvent():
    if timer is None: return
    timer.cancel()
    scheduleNextEvent()



#========== SCHEDULING ROUTINE ==========

def scheduleNextEvent():
    events = findNextEvents()
    if not events:
        logger.log("nothing to schedule, no events")
        return

    minutesToNextEvent = getMinutesToNextEvent(events[0])
    
    logger.log("scheduleding for:", events, ", in ", minutesToNextEvent, " miniutes")
    scheduleEvents(events, minutesToNextEvent)


def findNextEvents():
    nextEvents = []
    nextEventTime = None

    for event in eventsHandler.events:
        eventTime = addRelevantDaysToEvent(event)

        if eventTime == nextEventTime:
            nextEvents.append(event)
        elif nextEventTime is None or eventTime < nextEventTime:
            nextEvents.clear()
            nextEvents.append(event)
            nextEventTime = eventTime

    return nextEvents


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


def scheduleEvents(event, minutesFromNow):
    global timer

    if not timer is None: timer.cancel()
    timer = Timer(minutesFromNow * 60, lambda: performEventsAndScheduleNext(event))
    timer.start()


#========== OTHER ==========

def findEvent(eventName: str) -> dict:
    events = events.getStorageContentCopy()["events"]
    for event in events:
        if event["name"] == eventName:
            return event


#========== PERFORM EVENT ==========

def performEvents(events):
    for event in events:
        try:
            logger.log(f"performing event: {event}")
            TradfriInterface().commandRouter(event["device"], event["command"], event["payload"])
        except Exception as e:
            logger.log(f"   failed because: ", e)

        time.sleep(3)