from .tradfri_action import TradfriAction


class TradfriActionSuccess(TradfriAction):
    def __init__(self, msg = None) -> None:
        self.msg = msg

    def execute(self) -> str:
        return {"result": None, "msg": self.msg}

    def getDidSucceed(self) -> bool:
        return True