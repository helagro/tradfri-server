from http.server import BaseHTTPRequestHandler
import json
from . import router
from urllib import parse
import logger

class ReqHandler(BaseHTTPRequestHandler):

    #========== GET ==========

    def do_GET(self):
        try:
            query: dict = self.getQuery(self.path)
            
            response = router.route(query)
            self.setGETResponse(response)
        except Exception as e:
            logger.log("req_handler exception:", e, self.path)


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
