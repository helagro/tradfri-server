from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
import uuid
from settings.settings import Settings


class TradfriHandler:
    _CONFIG_PATH = "tradfri/tradfri_standalone_psk.conf"
    _GATEWAY_ADDR = Settings().getGatewayAddr()

    _gateway = None
    _api = None


    #========== CONSTRUCTOR ==========
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TradfriHandler, cls).__new__(cls)
        return cls.instance
    

    def __init__(self):
        self.doSetups()


    def doSetups(self):
        key = self._getKey()
        self._setup(key)



    def doAPI(self, command):
        return self._api(command)


    def getGateway(self):
        return self._gateway



    #========== HANDLE ARGUMENTS ==========

    def _getKey(self) -> None:
        if self._GATEWAY_ADDR not in load_json(self._CONFIG_PATH):
            print(
                "Please provide the 'Security Code' on the back of your " "Tradfri gateway:",
                end=" ",
            )
            key = input().strip()
            if len(key) != 16:
                raise PytradfriError("Invalid 'Security Code' provided.")
            
            return key



    #========== SETUP ==========

    def _setup(self, key):
        conf = load_json(self._CONFIG_PATH)

        try:
            identity = conf[self._GATEWAY_ADDR].get("identity")
            psk = conf[self._GATEWAY_ADDR].get("key")
            api_factory = APIFactory(host=self._GATEWAY_ADDR, psk_id=identity, psk=psk)
        except KeyError:
            identity = uuid.uuid4().hex
            api_factory = APIFactory(host=self._GATEWAY_ADDR, psk_id=identity)

            try:
                psk = api_factory.generate_psk(key)
                print("Generated PSK: ", psk, flush=True)

                conf[self._GATEWAY_ADDR] = {"identity": identity, "key": psk}
                save_json(self._CONFIG_PATH, conf)
            except AttributeError:
                raise PytradfriError(
                    "Please provide the 'Security Code' on the "
                    "back of your Tradfri gateway using the "
                    "-K flag."
                )

        self._api = api_factory.request
        self._gateway = Gateway()