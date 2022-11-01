from .tradfri_action import TradfriAction


class TradfriActionSuccess(TradfriAction):
    def execute(self) -> str:
        {"result": None}

    def getDidSucceed(self) -> bool:
        return True