from mimetypes import init
import threading
import time
from .tradfri_action.tradfri_action_command import TradfriActionCommand
from .tradfri_action.tradfri_action_success import TradfriActionSuccess
from .tradfri_action.tradfri_action_get_value import TradfriActionGetValue
from .tradfri_handler import TradfriHandler
from .tradfri_action.tradfri_action_fail import TradfriActionFail
import logs


class TradfriInterface:

    def __init__(self) -> None:
        self.tradfriHandler = TradfriHandler()


    def performAction(self, deviceID, action, payload):
        device = self.getDevice(deviceID)

        tradfriAction = self.actionRouter(device, deviceID, action, payload)
        result = tradfriAction.execute()
        didSucceed = tradfriAction.getDidSucceed()

        logs.log(f"Performed action '{action}' for '{deviceID}' with payload '{str(payload)}'"
            + f" with and didSucceed={didSucceed}")
        return result

    def actionRouter(self, device, deviceID, action, payload):
        match action:
            case "tOn":
                self.performAction(deviceID, "setState", 1)
                threading.Timer(3600, lambda: self.performAction(deviceID, "setState", 0)).start()
                return TradfriActionSuccess()
            case "getColor": 
                color = device.light_control.lights[0].hex_color
                return TradfriActionGetValue(valueName="color", value=color)
            case "getBrightness":
                brightness = device.light_control.lights[0].dimmer
                return TradfriActionGetValue(valueName="brightness", value=brightness)
            case "setBrightness": 
                command = device.light_control.set_dimmer(int(payload))
                return TradfriActionCommand(command)
            case "setBrightnessLevel":
                isOn = self.isOn()
                self.performAction(deviceID, "setBrightness", payload)
                time.sleep(3)
                self.performAction(deviceID, "setState", isOn)
            case "setColor": 
                command = device.light_control.set_hex_color(payload)
                return TradfriActionCommand(command)
            case "setDefinedColor": 
                command = device.light_control.set_predefined_color(payload)
                return TradfriActionCommand(command)
            case "setState":
                deviceControl = device.light_control if(device.has_light_control) else device.socket_control
                state = payload if (payload != "toggle") else (not self.performAction(deviceID, "isOn", None))
                command = deviceControl.set_state(state)
                return TradfriActionCommand(command)
            case _:
                return TradfriActionFail()


    def isOn(self, deviceID):
        device = self.getDevice(deviceID)
        if device.has_light_control:
            return device.light_control.lights[0].state
        if device.has_socket_control:
            return device.socket_control.sockets[0].state
        raise Exception("Invalid device")


    #========== GET DEVICE ==========
        
    def getDevices(self):
        devices_command = self.tradfriHandler.gateway.get_devices()
        devices_commands = self.tradfriHandler.api(devices_command)
        devices = self.tradfriHandler.api(devices_commands)

        devicesSerializable = []
        for device in devices:
            if(device.has_socket_control or device.has_light_control):
                devicesSerializable.append(dict(
                    id=device.id,
                    name=device.name  
                ))


        return devicesSerializable


    def getDevice(self, deviceID):
        device_command = self.tradfriHandler.gateway.get_device(deviceID)
        device = self.tradfriHandler.api(device_command)
        return device

