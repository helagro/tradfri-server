from .tradfri_action import TradfriAction


class TradfriActionGetValue(TradfriAction):
    def __init__(self, valueName, value):
        self.valueName = valueName
        self.value = value

    def execute(self) -> str:
        return {self.valueName: self.value}