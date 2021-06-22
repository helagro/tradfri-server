from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import file_manager

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def getQuery(self, path):
        return parse.parse_qs(parse.urlsplit(path).query)

    def queryRouter(self, query):
        if(len(query) == 0):
            return 


    def locationRouter(self, location):
        fileInfo = file_manager.getFile(location)
        return fileInfo


    def router(self, query, location):
        print(query, location)
        queryRouterRes = self.queryRouter(query)

        if(queryRouterRes is None):
            print("no queries")

        fileInfo = self.locationRouter(location)
        return fileInfo

        


    def do_GET(self):
        query = self.getQuery(self.path)
        location = self.path.split("?")[0]
        
        fileInfo = self.router(query, location)
        resCode = fileInfo["resCode"]

        self.send_response(resCode)

        if(resCode != 200):
            return

        self.send_header('Content-type', fileInfo["mimeType"])
        self.end_headers()


        self.wfile.write(fileInfo["fileContent"])

