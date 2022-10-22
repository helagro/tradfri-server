from .my_response import MyResponse

class MyResponseSuccessful(MyResponse):
    mimeType: str
    fileContent: bytes

    def __init__(self, mimeType, fileContent):
        super().__init__(200)
        self.mimeType = mimeType
        self.fileContent = fileContent

    @classmethod
    def empty(self):
        super().__init__(200)