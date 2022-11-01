from http.server import HTTPServer
import threading
from server.req_handler import ReqHandler
import events
import logs
from settings import sync_settings
import schedule

VERSION = "1.1"


def startServer():
    httpd = HTTPServer(('0.0.0.0', 8000), ReqHandler)
    httpd.serve_forever()
def startServerThread():
    t = threading.Thread(target=startServer)
    t.start()

def startSyncThread():
    t = threading.Thread(target=startSyncing)
    t.start()
def startSyncing():
    sync_settings.sync()
    schedule.every().day.at("01:00").do(sync_settings.sync)

def startRoutinedThread():
    t = threading.Thread(target=events.start)
    t.start()

if __name__ == "__main__":
    startServerThread()
    startSyncThread()
    startRoutinedThread()
    logs.log(f"Successfull tradfri setup; Version: {VERSION}")