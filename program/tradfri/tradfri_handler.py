from cgitb import reset
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
import argparse
import logs
import threading

CONFIG_FILE = "tradfri/tradfri_standalone_psk.conf"
gateway = None
api = None
args = None


#========== INPUT ==========

def getInput():
    global args
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "host", metavar="IP", type=str, help="IP Address of your Tradfri gateway"
    )
    parser.add_argument(
        "-K",
        "--key",
        dest="key",
        required=False,
        help="Security code found on your Tradfri gateway",
    )
    args = parser.parse_args()

    if args.host not in load_json(CONFIG_FILE) and args.key is None:
        print(
            "Please provide the 'Security Code' on the back of your " "Tradfri gateway:",
            end=" ",
        )
        key = input().strip()
        if len(key) != 16:
            raise PytradfriError("Invalid 'Security Code' provided.")
        else:
            args.key = key

getInput()


#========== SETUP ==========

def setup():
    global gateway
    global api

    conf = load_json(CONFIG_FILE)

    try:
        identity = conf[args.host].get("identity")
        psk = conf[args.host].get("key")
        api_factory = APIFactory(host=args.host, psk_id=identity, psk=psk)
    except KeyError:
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=args.host, psk_id=identity)

        try:
            psk = api_factory.generate_psk(args.key)
            print("Generated PSK: ", psk)

            conf[args.host] = {"identity": identity, "key": psk}
            save_json(CONFIG_FILE, conf)
        except AttributeError:
            raise PytradfriError(
                "Please provide the 'Security Code' on the "
                "back of your Tradfri gateway using the "
                "-K flag."
            )

    api = api_factory.request
    gateway = Gateway()


#========== PERFORM ACTION ==========

def performAction(deviceID, action, payload):
    device = getDevice(deviceID)
    deviceControl = device.light_control if(device.has_light_control) else device.socket_control
    result = None

    match action:
        case "tOn":
            performAction(deviceID, "setState", 1)
            threading.Timer(3600, lambda: performAction(deviceID, "setState", 0)).start()
        case "getColor": 
            result = {"color": device.light_control.lights[0].hex_color}
        case "isOn":
            result =  deviceControl.lights[0].state if device.has_light_control else deviceControl.sockets[0].state
        case _:
            actionPerformedSuccessfully = performActionWithCommand(device, deviceID, deviceControl, action, payload)
            if not actionPerformedSuccessfully: 
                FAILED_MESSAGE = "Failed to perform action " + action
                logs.log(FAILED_MESSAGE)
                return {"result": FAILED_MESSAGE}
            return {"result": f"Action '{action}' performed successfully with payload '{payload}'"}

    logs.log(f"Performed action \"{action}\" for \"{deviceID}\" with payload \"{str(payload)}\"")
    return result


def performActionWithCommand(device, deviceID, deviceControl, action, payload) -> bool:
    command = getCommand(device, deviceID, deviceControl, action, payload)
    if(command is None): 
        return False
    api(command)
    return True

def getCommand(device, deviceID, deviceControl, action: str, payload):
    match action:
        case "setBrightness": return device.light_control.set_dimmer(int(payload))
        case "setColor": return device.light_control.set_hex_color(payload)
        case "setDefinedColor": return device.light_control.set_predefined_color(payload)
        case "setState":
            state = payload if (payload != "toggle") else (not performAction(deviceID, "isOn", None))
            return deviceControl.set_state(state)


#========== GET DEVICE ==========
    
def getDevices():
    devices_command = gateway.get_devices()
    devices_commands = api(devices_command)
    devices = api(devices_commands)

    devicesSerializable = []
    for device in devices:
        if(device.has_socket_control or device.has_light_control):
            devicesSerializable.append(dict(
                id=device.id,
                name=device.name  
            ))


    return devicesSerializable


def getDevice(deviceID):
    device_command = gateway.get_device(deviceID)
    device = api(device_command)
    return device




setup()
