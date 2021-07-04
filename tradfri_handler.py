from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
import argparse
import threading

CONFIG_FILE = "tradfri_standalone_psk.conf"
gateway = None
api = None


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



def run():
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


def getDevice(deviceId):
    device_command = gateway.get_device(deviceId)
    device = api(device_command)
    return device




def performAction(deviceId, action, payload):
    device = getDevice(deviceId)

    deviceControl = device.light_control if(device.has_light_control) else device.socket_control

    command = None
    if(action == "setState"):
        command = deviceControl.set_state(payload)
    elif(action == "setBrightness"):
        command = device.light_control.set_dimmer(int(payload))
    elif(action == "setColor"):
        command = device.light_control.set_hex_color(payload)
    elif(action == "setDefinedColor"):
        command = device.light_control.set_predefined_color(payload)
    elif(action == "isOn"):
        return deviceControl.lights[0].state
    elif(action == "tOn"):
        performAction(deviceId, "setState", 1)
        threading.Timer(3600, lambda: performAction(deviceId, "setState", 0)).start()
        return
    else:
        print("Invalid action")
        return


    api(command)






run()
