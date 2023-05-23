import threading
import time
from .tradfri_handler import TradfriHandler
import logger
import traceback


class TradfriInterface:
    _TIME_BETWEEN_REQUESTS = 3
    _TF = TradfriHandler()


    def getDevices(self):
        devices_command = self._TF.getGateway().get_devices()
        devices_commands = self._TF.doAPI(devices_command)
        devices = self._TF.doAPI(devices_commands)

        devicesSerializable = []
        for device in devices:
            if(device.has_socket_control or device.has_light_control):
                devicesSerializable.append(dict(
                    id=device.id,
                    name=device.name  
                ))

        return devicesSerializable


    def getDevice(self, deviceID):
        device_command = self._TF.getGateway().get_device(deviceID)
        device = self._TF.doAPI(device_command)
        return device



    def commandRouter(self, deviceID, command, payload) -> dict:
        device = self.getDevice(deviceID)

        try:
            return self._commandRouterHelper(device, deviceID, command, payload)
        except Exception:
            logger.log(f"{command} for {deviceID} with {payload} failed: {traceback.format_exc()}")
            return {"resCode": 500}



    def _commandRouterHelper(self, device, deviceID, command, payload) -> dict:
        if command == "getBrightness":
            return self.getBrightness(device)
        
        elif command == "getColor": 
            return self.getColor(device)

        elif command == "setBrightness": 
            return self._TF.doAPI(
                device.light_control.set_dimmer(int(payload))
            )

        elif command == "setBrightnessLevel":
            wasOn = self.isOn(deviceID)
            self.commandRouter(deviceID, "setBrightness", payload)
            
            if not wasOn: 
                time.sleep(self._TIME_BETWEEN_REQUESTS)
                self.commandRouter(deviceID, "setState", False)

        elif command == "setColor": 
            return self._TF.doAPI(
                device.light_control.set_hex_color(payload)
            )

        elif command == "setDefinedColor": 
            return self._TF.doAPI(
                device.light_control.set_predefined_color(payload)
            )

        elif command == "setState":
            deviceControl = device.light_control if(device.has_light_control) else device.socket_control
            state = payload if (payload != "toggle") else not self.isOn(deviceID)
            return self._TF.doAPI(
                deviceControl.set_state(state)
            )

        elif command == "tOn":
            self.commandRouter(deviceID, "setState", 1)
            threading.Timer(3600, lambda: self.commandRouter(deviceID, "setState", 0)).start()

        elif command == "turnOffIf":
            brightness = self.commandRouter(deviceID, "getBrightness", None)["brightness"]
            if int(payload) == brightness:
                return self._commandRouterHelper(device, deviceID, "setState", False)
            return {"msg": f"{payload} != {brightness}"}

        elif command == "wakeUp":
            if self.isOn(deviceID): 
                return {"msg": "Lamp was already on, aborting..."}
            else: 
                return self._commandRouterHelper(device, deviceID, "setBrightness", payload)


        # ====== BETA =====
        # elif command == "observe":
        #     cmd2 = device.observe(self.callback, self.err_callback)
        #     logger.log("started observing", deviceID, cmd2)
        #     self._TF.doAPI(cmd2)

        # elif command == "raw":
        #     deviceControl = device.light_control if(device.has_light_control) else device.socket_control
        #     logger.log("raw", deviceControl.raw, device.reachable, device.last_seen)
        #     # return self.tradfriHandler.api(
        #     #     device.light_control.raw
        #     # )


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