from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
import argparse
from settings.settings import Settings
import logger


class TradfriHandler:
    CONFIG_PATH = "tradfri/tradfri_standalone_psk.conf"
    gatewayAddr = Settings().gatewayAddr
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
            "-K",
            "--key",
            dest="key",
            required=False,
            help="Security code found on your Tradfri gateway",
        )
        args = parser.parse_args()

        if self.gatewayAddr not in load_json(self.CONFIG_PATH) and args.key is None:
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
        conf = load_json(self.CONFIG_PATH)

        try:
            identity = conf[self.gatewayAddr].get("identity")
            psk = conf[self.gatewayAddr].get("key")
            api_factory = APIFactory(host=self.gatewayAddr, psk_id=identity, psk=psk)
        except KeyError:
            identity = uuid.uuid4().hex
            api_factory = APIFactory(host=self.gatewayAddr, psk_id=identity)

            try:
                psk = api_factory.generate_psk(args.key)
                print("Generated PSK: ", psk)

                conf[self.gatewayAddr] = {"identity": identity, "key": psk}
                save_json(self.CONFIG_PATH, conf)
            except AttributeError:
                raise PytradfriError(
                    "Please provide the 'Security Code' on the "
                    "back of your Tradfri gateway using the "
                    "-K flag."
                )

        self.api = api_factory.request
        self.gateway = Gateway()