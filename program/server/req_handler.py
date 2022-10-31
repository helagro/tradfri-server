from http.server import BaseHTTPRequestHandler
from .my_response import MyResponse
from .my_response_successful import MyResponseSuccessful
from .my_mime_types import MyMimeTypes
from . import router
from urllib import parse
import json
from cgi import parse_header, parse_multipart
from settings.storage_handler import StorageHandler

class ReqHandler(BaseHTTPRequestHandler):

    #========== GET ==========

    def do_GET(self):
        query: dict = self.getQuery(self.path)
        location: str = self.path.split("?")[0]
        
        response: MyResponse = router.route(location, query)
        self.setGETResponse(response)

    def getQuery(self, path):
        return parse.parse_qs(parse.urlsplit(path).query)

    def setGETResponse(self, response: MyResponse):
        self.send_response(response.resCode)

        if not  isinstance(response, MyResponseSuccessful):
            self.end_headers()
            return

        self.send_header('Content-type', response.mimeType.value)
        self.end_headers()
        self.wfile.write(response.fileContent)


    #========== POST ==========

    def do_POST(self):
        infoReceived = self.parse_POST()
        jsonArea = infoReceived[b'jsonArea'][0]
        jsonObj = self.getJsonObject(jsonArea)
        
        storageHandler = StorageHandler()
        storageHandler.calculateTimeInMin(jsonObj)
        storageHandler.saveInputStorageContent(jsonObj)

        self.send_response(301)
        self.send_header("location", "/index.html")
        self.send_header('Content-type', MyMimeTypes.HTML)
        self.end_headers()

        myResponse = router.route("", "/")
        if isinstance(myResponse, MyResponseSuccessful):  
            self.wfile.write(myResponse.fileContent)

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            return parse_multipart(self.rfile, pdict)
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            return parse.parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        return {}

    def getJsonObject(self, jsonArea):
        jsonAreaStr = jsonArea.decode("utf-8")
        return json.loads(jsonAreaStr)

        



