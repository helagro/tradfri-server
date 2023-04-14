import threading
import time
from .tradfri_handler import TradfriHandler
import logger
import traceback


class TradfriInterface:
    TIME_BETWEEN_REQUESTS = 3
    tradfriHandler = TradfriHandler()


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




    def commandRouter(self, deviceID, command, payload):
        device = self.getDevice(deviceID)

        try:
            return self.commandRouterHelper(device, deviceID, command, payload)
        except Exception:
            logger.log(f"{command} for {deviceID} with {payload} failed: {traceback.format_exc()}")
            return {"resCode": 500}



    def commandRouterHelper(self, device, deviceID, command, payload):
        if command == "getBrightness":
            return self.getBrightness(device)
        
        elif command == "getColor": 
            return self.getColor(device)

        elif command == "setBrightness": 
            return self.tradfriHandler.api(
                device.light_control.set_dimmer(int(payload))
            )

        elif command == "setBrightnessLevel":
            wasOn = self.isOn(deviceID)
            self.commandRouter(deviceID, "setBrightness", payload)
            
            if not wasOn: 
                time.sleep(self.TIME_BETWEEN_REQUESTS)
                self.commandRouter(deviceID, "setState", False)

        elif command == "setColor": 
            return self.tradfriHandler.api(
                device.light_control.set_hex_color(payload)
            )

        elif command == "setDefinedColor": 
            return self.tradfriHandler.api(
                device.light_control.set_predefined_color(payload)
            )

        elif command == "setState":
            deviceControl = device.light_control if(device.has_light_control) else device.socket_control
            state = payload if (payload != "toggle") else not self.isOn(deviceID)
            return self.tradfriHandler.api(
                deviceControl.set_state(state)
            )

        elif command == "tOn":
            self.commandRouter(deviceID, "setState", 1)
            threading.Timer(3600, lambda: self.commandRouter(deviceID, "setState", 0)).start()

        elif command == "turnOffIf":
            brightness = self.commandRouter(deviceID, "getBrightness", None)["brightness"]
            if int(payload) == brightness:
                return self.commandRouterHelper(device, deviceID, "setState", False)
            return {"msg": f"{payload} != {brightness}"}

        elif command == "wakeUp":
            if self.isOn(deviceID): 
                return {"msg": "Lamp was already on, aborting..."}
            else: 
                return self.commandRouterHelper(device, deviceID, "setBrightness", payload)


        # ====== BETA =====
        elif command == "observe":
            cmd2 = device.observe(self.callback, self.err_callback)
            logger.log("started observing", deviceID, cmd2)
            TradfriHandler().api(cmd2)


        else:
            return {"resCode": 404}


    def isOn(self, deviceID):
        device = self.getDevice(deviceID)
        if device.has_light_control:
            return device.light_control.lights[0].state
        if device.has_socket_control:
            return device.socket_control.sockets[0].state
        raise Exception("Invalid device")

    def getBrightness(self, device):
        brightness = device.light_control.lights[0].dimmer
        return {"brightness": brightness}

    def getColor(self, device):
        color = device.light_control.lights[0].hex_color
        return {"color": color}




    def callback(self, updated_device):
        light = updated_device.light_control.lights[0]
        print(f"Received message for: {light}")

    def err_callback(self, err: Exception) -> None:
        print(err)