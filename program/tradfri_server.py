from http.server import HTTPServer
import threading
from server.req_handler import ReqHandler
import tradfri.timers as timers
import tradfri.tradfri_handler as tradfri_handler
import logs
from settings import sync_settings


def startServer():
    httpd = HTTPServer(('0.0.0.0', 8000), ReqHandler)
    httpd.serve_forever()

def startServerThread():
    t = threading.Thread(target=startServer)
    t.start()



def startRoutinedThread():
    t = threading.Thread(target=timers.start)
    t.start()

if __name__ == "__main__":
    tradfri_handler.setup()

    startServerThread()
    startRoutinedThread()
    sync_settings.sync()
    logs.log("Successfull tradfri setup")