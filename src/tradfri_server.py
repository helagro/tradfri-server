from http.server import HTTPServer
import threading
import time
from server.req_handler import ReqHandler
import schedule
import logger
import settings.sync_events as sync_events
import schedule

VERSION = "1.11"


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
    sync_events.sync()
    schedule.every().day.at("01:00").do(sync_events.sync)
    while True: 
        time.sleep(30*60)
        schedule.run_pending()


def startRoutinedThread():
    t = threading.Thread(target=schedule.start)
    t.start()

if __name__ == "__main__":
    startServerThread()
    startSyncThread()
    startRoutinedThread()
    logger.log(f"Successfull tradfri setup; Version: {VERSION}")