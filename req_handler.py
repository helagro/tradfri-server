from http.server import HTTPServer, BaseHTTPRequestHandler
import input_router
from urllib import parse
import json
from cgi import parse_header, parse_multipart
import storage_handler

class ReqHandler(BaseHTTPRequestHandler):
    
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

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse.parse_qs(
                    self.rfile.read(length), 
                    keep_blank_values=1)
        else:
            postvars = {}
        return postvars

    def do_POST(self):
        infoSent = self.parse_POST()
        jsonArea = infoSent[b'jsonArea'][0]
        jsonAreaStr = jsonArea.decode("utf-8")
        jsonObj = json.loads(jsonAreaStr)
        storage_handler.saveInputStorageContent(jsonObj)

        self.send_response(301)
        self.send_header("location", "/index.html")
        self.send_header('Content-type', "text/html")
        self.end_headers()


        self.wfile.write(input_router.entry("", "/")["fileContent"])

        



