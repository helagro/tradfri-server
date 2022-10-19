from http.server import HTTPServer
import threading
from req_handler import ReqHandler
import tradfri.timers as timers
import tradfri.tradfri_handler as tradfri_handler
import logs


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
    tradfri_handler.run()

    startServerThread()
    startRoutinedThread()
    logs.log("Successfull tradfri setup")