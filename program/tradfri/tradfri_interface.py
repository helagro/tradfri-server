
from mimetypes import init

from program.tradfri.tradfri_handler import TradfriHandler


class TradfriInterface:

    def __init__(self) -> None:
        self.tradfriHandler = TradfriHandler()


    def performAction(self, deviceID, action, payload):
        device = getDevice(deviceID)
        deviceControl = device.light_control if(device.has_light_control) else device.socket_control
        result = None

        match action:
            case "tOn":
                performAction(deviceID, "setState", 1)
                threading.Timer(3600, lambda: performAction(deviceID, "setState", 0)).start()
            case "getColor": 
                result = {"color": device.light_control.lights[0].hex_color}
            case "getBrightness":
                result = {"brightness": device.light_control.lights[0].dimmer}
            case "isOn":
                result =  deviceControl.lights[0].state if device.has_light_control else deviceControl.sockets[0].state
            case _:
                actionPerformedSuccessfully = performActionWithCommand(device, deviceID, deviceControl, action, payload)
                if not actionPerformedSuccessfully: 
                    FAILED_MESSAGE = "Failed to perform action " + action
                    logs.log(FAILED_MESSAGE)
                    return {"result": FAILED_MESSAGE}
                result = {"result": f"Action '{action}' performed successfully with payload '{payload}'"}

        logs.log(f"Performed action \"{action}\" for \"{deviceID}\" with payload \"{str(payload)}\"")
        return result


    def performActionWithCommand(self, device, deviceID, deviceControl, action, payload) -> bool:
        command = getCommand(device, deviceID, deviceControl, action, payload)
        if(command is None): 
            return False
        api(command)
        return True

    def getCommand(self, device, deviceID, deviceControl, action: str, payload):
        match action:
            case "setBrightness": return device.light_control.set_dimmer(int(payload))
            case "setColor": return device.light_control.set_hex_color(payload)
            case "setDefinedColor": return device.light_control.set_predefined_color(payload)
            case "setState":
                state = payload if (payload != "toggle") else (not performAction(deviceID, "isOn", None))
                return deviceControl.set_state(state)


    #========== GET DEVICE ==========
        
    def getDevices(self):
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


    def getDevice(self, deviceID):
        device_command = gateway.get_device(deviceID)
        device = api(device_command)
        return device

