from event.events import Events
from datetime import datetime
from threading import Timer
import logger
import time
from tradfri.tradfri_interface import TradfriInterface
import traceback

_EVENTS = Events()
_timer = None
_skipNextAt = None


#========== ENTRY POINTS ==========

def start():
    _EVENTS.addUpdateListener(rescheduleEvent)
    _scheduleNextEvent()


def performEventsAndScheduleNext(events):
    _performEvents(events)
    _scheduleNextEvent()


def rescheduleEvent():
    if _timer is None: return
    _timer.cancel()
    _scheduleNextEvent()



#========== SCHEDULING ROUTINE ==========

def _scheduleNextEvent():
    events = _findNextEvents()
    if not events:
        logger.log("nothing to schedule, no events")
        return

    minutesToNextEvent = _getMinutesToNextEvent(events[0])
    
    logger.log("scheduleding:", events, ", in ", minutesToNextEvent, " miniutes")
    _scheduleEvents(events, minutesToNextEvent)


def _findNextEvents():
    nextEvents = []
    nextEventTime = None

    for event in _EVENTS.events:
        eventTime = _addRelevantDaysToEvent(event)

        if eventTime == nextEventTime:
            nextEvents.append(event)
        elif nextEventTime is None or eventTime < nextEventTime:
            nextEvents.clear()
            nextEvents.append(event)
            nextEventTime = eventTime

    return nextEvents


def _addRelevantDaysToEvent(event) -> int:
    currentTime = _getCurTimeInMin()

    if(event["time"] <= currentTime):
        return event["time"] + 24*60
    return event["time"]


def _getCurTimeInMin() -> int:
    now = datetime.now()
    return now.hour * 60 + now.minute


def _getMinutesToNextEvent(event) -> int:
    eventTime = event["time"]
    nowInMin = _getCurTimeInMin()
    day = 0 if nowInMin < eventTime else 24*60
    return eventTime + day - nowInMin


def _scheduleEvents(event, minutesFromNow):
    global _timer

    if not _timer is None: _timer.cancel()
    _timer = Timer(minutesFromNow * 60, lambda: performEventsAndScheduleNext(event))
    _timer.start()



#========== OTHER ==========

def _isSkipped(events) -> bool:
    return events and events[0]["time"] == _skipNextAt



#========== PERFORM EVENT ==========

def _performEvents(events):
    global _skipNextAt
    if _isSkipped(events):
        _skipNextAt = None
    else:
        for event in events:
            try:
                result = TradfriInterface().commandRouter(event["device"], event["command"], event["payload"])
                logger.log(f"performing event: {event} result: {result}")
            except Exception as e:
                logger.log(traceback.format_exc())

            time.sleep(3)


