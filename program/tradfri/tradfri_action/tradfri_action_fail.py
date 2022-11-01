from .tradfri_action import TradfriAction 

class TradfriActionFail(TradfriAction):

    def __init__(self, msg) -> None:
        self.msg = msg

    def execute(self) -> str:
        return {"success": False, "msg": self.msg}

    def getDidSucceed(self) -> bool:
        return False