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


    if(command == "devices"): 
        return tradfriInterface.getDevices()
    elif(command == "logs"): 
        return logger.getLogs()
    elif(command == "update"): 
        subprocess.Popen("bash_scripts/update.sh")
        sys.exit()
    elif(command == "events"):
        return Events().events
    elif(command == "doEvent"): 
        event_schedule.performEventByName(payload)
    else: 
        return tradfriInterface.commandRouter(device, command, payload)

