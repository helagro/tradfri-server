from tradfri.tradfri_interface import TradfriInterface
import logger
import event.event_schedule as event_schedule
from event.events import Events
import json

_TRADFRI_INTERFACE = TradfriInterface()


def route(location: dict):
    command = location["c"][0] if "c" in location else "usage"
    device = location["d"][0] if "d" in location else None
    payload = location["p"][0] if "p" in location else None

    return _routeHelper(command, device, payload)


def _routeHelper(command, device, payload):
    if command == "devices": 
        return _TRADFRI_INTERFACE.getDevices()

    elif command == "doNext":
        events = event_schedule._findNextEvents()
        event_schedule._performEvents(events)

    elif command == "events":
        return getEvents()

    elif command == "logs": 
        return logger.getLogs()

    elif command == "nextEvents":
        return nextEvents()

    elif command == "skipAt":
        skipAt(int(payload))
        return getEvents()

    elif command == "skipClear":
        event_schedule._skipNextAt = None
        return getEvents()

    elif command == "skipNext":
        events = event_schedule._findNextEvents()
        if events: skipAt(events[0]["time"])
        return nextEvents()

    elif command == "sync":
        Events().downloadEvents()
        return _TRADFRI_INTERFACE.commandRouter(None, "events", None)

    elif command == "usage" or command == "help" or command == "info":
        return usage()

    else: 
        return _TRADFRI_INTERFACE.commandRouter(device, command, payload)



def getEvents():
    return {
        "skipNextAt": event_schedule._skipNextAt,
        "events": Events().events
    }


def skipAt(time):
    event_schedule._skipNextAt = time


def nextEvents():
    nextEvents = event_schedule._findNextEvents()
    return {
        "willSkip": event_schedule._isSkipped(nextEvents),
        "events": nextEvents
    }


def usage():
    f = open("server/usage.json")
    usage = json.load(f)
    f.close()
    return usage