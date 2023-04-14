from http.server import HTTPServer
import threading
import time
from server.req_handler import ReqHandler
import schedule
from events import Events
import event_schedule
import argparse
from settings import options


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noDownload", action="store_true")
    args = parser.parse_args()

    options.noDownload = args.noDownload


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
    schedule.every().day.at("04:00").do(Events().downloadEvents)
    while True: 
        time.sleep(50*60)
        schedule.run_pending()


def startRoutinedThread():
    t = threading.Thread(target=event_schedule.start)
    t.start()



if __name__ == "__main__":
    parseArguments()

    startServerThread()
    startSyncThread()
    startRoutinedThread()