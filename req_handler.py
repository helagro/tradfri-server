from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import file_manager

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def getQuery(self, path):
        return parse.parse_qs(parse.urlsplit(self.path).query)

    def do_GET(self):
        query = self.getQuery(self.path)
        print(query)

        self.send_response(200)
        self.send_header('Content-type',    'text/html')
        self.end_headers()

        htmlPage = file_manager.getFile("index.html")

        self.wfile.write(htmlPage)

