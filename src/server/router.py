from tradfri.tradfri_interface import TradfriInterface
import logger
import subprocess
import sys
import event_schedule
from settings.events import Events

tradfriInterface = TradfriInterface()


def route(location: dict):
    command = location["c"][0]
    device = location["d"][0] if "d" in location else None
    payload = location["p"][0] if "p" in location else None


    if command == "devices": 
        return tradfriInterface.getDevices()
    elif command == "logs": 
        return logger.getLogs()
    elif command == "update": 
        subprocess.Popen("scripts/update.sh")
        sys.exit()
    elif command == "doNext":
        events = event_schedule.findNextEvents()
        event_schedule.performEvents(events)
    elif command == "sync":
        Events().downloadEvents()
    elif command == "events":
        return Events().events
    elif command == "nextEvent":
        return event_schedule.findNextEvents()
    else: 
        return tradfriInterface.commandRouter(device, command, payload)

