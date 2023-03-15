from settings.events import StorageHandler
from tradfri.tradfri_interface import TradfriInterface
import json
import logger
import subprocess
import sys
import schedule

tradfriInterface = TradfriInterface()


def route(location: dict):
    command = location["c"][0]
    device = location["d"][0] if "d" in location else None
    payload = location["p"][0] if "p" in location else None

    response = None
    resCode = 200

    if(command == "devices"): 
        response = tradfriInterface.getDevices()
    elif(command == "logs"): 
        response = logger.getLogs()
    elif(command == "update"): 
        subprocess.Popen("bash_scripts/update.sh")
        sys.exit()
    elif(command == "doEvent"): 
        schedule.performEventByName(payload)
    else: 
        return tradfriInterface.performAction(device, command, payload)


    return {
        "response": response,
        "resCode": resCode
    }

