from .tradfri_action import TradfriAction 

class TradfriActionFail(TradfriAction):
    def execute(self) -> str:
        return ""

    def getDidSucceed(self) -> bool:
        return False