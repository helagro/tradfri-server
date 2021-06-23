from http.server import HTTPServer, BaseHTTPRequestHandler
import input_router
from urllib import parse
from cgi import parse_header, parse_multipart

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
        print("vi har post ==============================================================")
        print(self.parse_POST())

