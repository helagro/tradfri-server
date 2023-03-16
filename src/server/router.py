from tradfri.tradfri_interface import TradfriInterface
import logger
import subprocess
import sys
import event_schedule

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
        response = logger.getLogs().replace("\n", "\r\n")
    elif(command == "update"): 
        subprocess.Popen("bash_scripts/update.sh")
        sys.exit()
    elif(command == "doEvent"): 
        event_schedule.performEventByName(payload)
    else: 
        response = tradfriInterface.commandRouter(device, command, payload)


    return {
        "response": response,
        "resCode": resCode
    }

