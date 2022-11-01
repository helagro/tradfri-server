from cgitb import reset
from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
import argparse


class TradfriHandler:
    CONFIG_FILE = "tradfri/tradfri_standalone_psk.conf"
    gateway = None
    api = None
    args = None


    #========== CONSTRUCTOR ==========
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TradfriHandler, cls).__new__(cls)
            cls.instance.doSetups()
        return cls.instance

    def doSetups(self):
        self.getInput()
        self.setup()


    #========== HANDLE ARGUMENTS ==========

    def getInput(self):
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

        if args.host not in load_json(self.CONFIG_FILE) and args.key is None:
            print(
                "Please provide the 'Security Code' on the back of your " "Tradfri gateway:",
                end=" ",
            )
            key = input().strip()
            if len(key) != 16:
                raise PytradfriError("Invalid 'Security Code' provided.")
            else:
                args.key = key


    #========== SETUP ==========

    def setup(self):
        conf = load_json(self.CONFIG_FILE)

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
                save_json(self.CONFIG_FILE, conf)
            except AttributeError:
                raise PytradfriError(
                    "Please provide the 'Security Code' on the "
                    "back of your Tradfri gateway using the "
                    "-K flag."
                )

        self.api = api_factory.request
        self.gateway = Gateway()