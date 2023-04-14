from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
from settings.settings import Settings
import logger


class TradfriHandler:
    CONFIG_PATH = "tradfri/tradfri_standalone_psk.conf"
    gatewayAddr = Settings().gatewayAddr
    gateway = None
    api = None
    key = None


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
        if self.gatewayAddr not in load_json(self.CONFIG_PATH):
            print(
                "Please provide the 'Security Code' on the back of your " "Tradfri gateway:",
                end=" ",
            )
            self.key = input().strip()
            if len(self.key) != 16:
                raise PytradfriError("Invalid 'Security Code' provided.")


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
                psk = api_factory.generate_psk(self.key)
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