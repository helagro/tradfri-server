from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import storage_handler
import uuid

CONFIG_FILE = "tradfri_standalone_psk.conf"

gateway = Gateway()
isSetup = False
api = None

key = None


def init():
    global key

    if load_json(CONFIG_FILE)["host"] is None:
        print(
            "Please provide the 'Security Code' on the back of your " "Tradfri gateway:",
            end=" ",
        )
        key = input().strip()
    if len(key) != 16:
        raise PytradfriError("Invalid 'Security Code' provided.")
    setup()


def setup(): 
    conf = load_json(CONFIG_FILE)

    try:
        identity = conf["host"].get("identity")
        psk = conf["host"].get("key")
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
    print("dev", devices)


storage_handler.storageContentUpdateListeners.append(setup)
setup()