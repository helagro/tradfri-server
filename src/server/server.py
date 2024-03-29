from http.server import BaseHTTPRequestHandler
import json
from . import router
from urllib import parse
import logger
import traceback

class MyServer(BaseHTTPRequestHandler):

    #========== GET ==========

    def do_GET(self):
        try:
            query: dict = self._getQuery(self.path)
            
            response = router.route(query)
            self._setGETResponse(response)
        except Exception as _:
            logger.log("req_handler exception:", traceback.format_exc())


    def _getQuery(self, path) -> dict:
        return parse.parse_qs(parse.urlsplit(path).query)


    def _setGETResponse(self, responseObj):
        if isinstance(responseObj, dict) and "resCode" in responseObj and responseObj["resCode"] != 200 :
            self.send_response(responseObj["resCode"])
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', "application/json")
        self.end_headers()

        responseStr = json.dumps(responseObj)
        response = responseStr.encode("utf-8")
        self.wfile.write(response)
