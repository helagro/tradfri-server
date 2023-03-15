from http.server import BaseHTTPRequestHandler


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


    def setGETResponse(self, response):
        self.send_response(200)

        if not isinstance(response, MyResponseSuccessful):
            self.end_headers()
            return

        self.send_header('Content-type', response.mimeType.value)
        self.end_headers()
        self.wfile.write(response.fileContent)
