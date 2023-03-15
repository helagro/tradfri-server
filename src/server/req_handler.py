from http.server import BaseHTTPRequestHandler
import json
from . import router
from urllib import parse
import logger

class ReqHandler(BaseHTTPRequestHandler):

    #========== GET ==========

    def do_GET(self):
        try:
            location: str = self.path.split("?")[0]
            
            response = router.route(location)
            self.setGETResponse(response)
        except Exception as e:
            logger.log(e, self.path)


    def getQuery(self, path):
        return parse.parse_qs(parse.urlsplit(path).query)


    def setGETResponse(self, responseObj):
        if responseObj == "error":
            self.send_response(500)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()

        responseStr = json.dumps(responseObj)
        response = responseStr.encode("utf-8")
        self.wfile.write(response)
