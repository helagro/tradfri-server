from mimetypes import init
import threading
import time
from .tradfri_action.tradfri_action_command import TradfriActionCommand
from .tradfri_action.tradfri_action_success import TradfriActionSuccess
from .tradfri_action.tradfri_action_get_value import TradfriActionGetValue
from .tradfri_handler import TradfriHandler
from .tradfri_action.tradfri_action_fail import TradfriActionFail
import logger


class TradfriInterface:

    def __init__(self) -> None:
        self.tradfriHandler = TradfriHandler()


    def performAction(self, deviceID, action, payload):
        device = self.getDevice(deviceID)

        tradfriAction = self.actionRouter(device, deviceID, action, payload)
        result = tradfriAction.execute()
        didSucceed = tradfriAction.getDidSucceed()

        logger.log(f"Performed action '{action}' for '{deviceID}' with payload '{str(payload)}'"
            + f" with and didSucceed={didSucceed} and result={result}")
        return result

    def actionRouter(self, device, deviceID, action, payload):
        if action == "tOn":
            self.performAction(deviceID, "setState", 1)
            threading.Timer(3600, lambda: self.performAction(deviceID, "setState", 0)).start()
            return TradfriActionSuccess()
        elif action == "getColor": 
            color = device.light_control.lights[0].hex_color
            return TradfriActionGetValue(valueName="color", value=color)
        elif action == "getBrightness":
            brightness = device.light_control.lights[0].dimmer
            return TradfriActionGetValue(valueName="brightness", value=brightness)
        elif action == "setBrightness": 
            command = device.light_control.set_dimmer(int(payload))
            return TradfriActionCommand(command)
        elif action == "wakeUp":
            isOn = self.isOn(deviceID)
            if isOn: 
                return TradfriActionSuccess("Lamp was already on, aborting...")
            else: 
                return self.actionRouter(device, deviceID, "setBrightness", payload)
        elif action == "setBrightnessLevel":
            isOn = self.isOn(deviceID)
            self.performAction(deviceID, "setBrightness", payload)
            time.sleep(3)
            self.performAction(deviceID, "setState", isOn)
            return TradfriActionSuccess()
        elif action == "setColor": 
            command = device.light_control.set_hex_color(payload)
            return TradfriActionCommand(command)
        elif action == "setDefinedColor": 
            command = device.light_control.set_predefined_color(payload)
            return TradfriActionCommand(command)
        elif action == "setState":
            deviceControl = device.light_control if(device.has_light_control) else device.socket_control
            state = payload if (payload != "toggle") else not self.isOn(deviceID)
            command = deviceControl.set_state(state)
            return TradfriActionCommand(command)
        elif action == "turnOffIf":
            brightness = self.performAction(deviceID, "getBrightness", None)["brightness"]
            if int(payload) == brightness:
                return self.actionRouter(device, deviceID, "setState", False)
            return TradfriActionSuccess(msg=f"{payload} != {brightness}")
        else:
            return TradfriActionFail(msg="Invalid Action")


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

