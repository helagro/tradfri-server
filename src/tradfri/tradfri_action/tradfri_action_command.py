from sre_constants import SUCCESS
from ..tradfri_handler import TradfriHandler
from .tradfri_action import TradfriAction
import logger

class TradfriActionCommand(TradfriAction):
    def __init__(self, command) -> None:
        self.command = command
        self.tradfriHandler = TradfriHandler()

    def execute(self) -> str:
        if self.command is None:
            self.fail()
            return {"success": False}
        result = self.tradfriHandler.api(self.command)
        self.didSucceed = True
        return {"success":True}

    def fail(self):
        self.didSucceed = False
        logger.log("Failed to perform action")