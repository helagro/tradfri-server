from http.server import HTTPServer, BaseHTTPRequestHandler
import input_router
from urllib import parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def getQuery(self, path):
        return parse.parse_qs(parse.urlsplit(path).query)

    def do_GET(self):
        query = self.getQuery(self.path)
        location = self.path.split("?")[0]
        
        fileInfo = input_router.entry(query, location)
        resCode = fileInfo["resCode"]

        self.send_response(resCode)

        if(resCode != 200):
            return

        self.send_header('Content-type', fileInfo["mimeType"])
        self.end_headers()


        self.wfile.write(fileInfo["fileContent"])

