from abc import ABC, abstractmethod

class TradfriAction(ABC):    
    @abstractmethod
    def execute(self) -> str:
        pass

    def getDidSucceed(self) -> bool:
        return True