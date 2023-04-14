from tradfri.tradfri_interface import TradfriInterface
import logger
import subprocess
import sys
import event.event_schedule as event_schedule
from event.events import Events
import json
from threading import Timer

tradfriInterface = TradfriInterface()

def route(location: dict):
    command = location["c"][0] if "c" in location else None
    device = location["d"][0] if "d" in location else None
    payload = location["p"][0] if "p" in location else None

    if not command:
        command = "usage"

    return routeHelper(command, device, payload)



def routeHelper(command, device, payload):
    if command == "devices": 
        return tradfriInterface.getDevices()

    elif command == "doNext":
        events = event_schedule.findNextEvents()
        event_schedule.performEvents(events)

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
        event_schedule.skipNextAt = None
        return getEvents()

    elif command == "skipNext":
        events = event_schedule.findNextEvents()
        if events: skipAt(events[0]["time"])
        return nextEvents()

    elif command == "sync":
        Events().downloadEvents()
        return tradfriInterface.commandRouter(None, "events", None)

    elif command == "update": 
        Timer(2.0, doUpdate).start()
        return "updating..., refresh in 10 seconds"

    elif command == "usage" or command == "help" or command == "info":
        return usage()

    else: 
        return tradfriInterface.commandRouter(device, command, payload)



def getEvents():
    return {
        "skipNextAt": event_schedule.skipNextAt,
        "events": Events().events
    }


def skipAt(time):
    event_schedule.skipNextAt = time


def doUpdate():
    subprocess.Popen("scripts/update.sh")
    sys.exit() 


def nextEvents():
    nextEvents = event_schedule.findNextEvents()
    return {
        "willSkip": event_schedule.isSkipped(nextEvents),
        "events": nextEvents
    }


def usage():
    f = open("server/usage.json")
    usage = json.load(f)
    f.close()
    return usage