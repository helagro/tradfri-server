from tradfri.tradfri_interface import TradfriInterface
import logger
import subprocess
import sys
import event_schedule
from events import Events
import json
from threading import Timer

tradfriInterface = TradfriInterface()


def route(location: dict):
    command = location["c"][0] if "c" in location else None
    device = location["d"][0] if "d" in location else None
    payload = location["p"][0] if "p" in location else None

    if not command:
        command = "usage"


    if command == "devices": 
        return tradfriInterface.getDevices()
    elif command == "doNext":
        events = event_schedule.findNextEvents()
        event_schedule.performEvents(events)
    elif command == "events":
        return Events().events
    elif command == "logs": 
        return logger.getLogs()
    elif command == "nextEvents":
        return event_schedule.findNextEvents()
    elif command == "sync":
        Events().downloadEvents()
    elif command == "update": 
        Timer(2.0, doUpdate).start()
        return "updating..., refresh in 10 seconds"
    elif command == "usage" or command == "help" or command == "info":
        f = open("usage.json")
        return json.load(f) 
    else: 
        return tradfriInterface.commandRouter(device, command, payload)

def doUpdate():
    subprocess.Popen("scripts/update.sh")
    sys.exit() 
