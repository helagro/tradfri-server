from tradfri.tradfri_interface import TradfriInterface
import logger
import subprocess
import sys
import event_schedule
from events import Events
import json

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
        subprocess.Popen("scripts/update.sh")
        sys.exit()  
    elif command == "usage" | command == "help":
        f = open("usage.json")
        return json.load(f) 
    else: 
        return tradfriInterface.commandRouter(device, command, payload)

