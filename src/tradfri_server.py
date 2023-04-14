from http.server import HTTPServer
import threading
from server.req_handler import ReqHandler
import event.event_schedule as event_schedule
import argparse
import logger
from event import sync


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noDownload", action="store_true")
    args = parser.parse_args()

    if args.noDownload: logger.log("will not download events", args.noDownload)

    return args.noDownload


def startServer():
    httpd = HTTPServer(('0.0.0.0', 8000), ReqHandler)
    httpd.serve_forever()

def startServerThread():
    t = threading.Thread(target=startServer)
    t.start()


def startSyncThread():
    t = threading.Thread(target=sync.scheduleSync)
    t.start()



def startRoutinedThread():
    t = threading.Thread(target=event_schedule.start)
    t.start()



if __name__ == "__main__":
    noDownloads = parseArguments()
    if not noDownloads: sync.sync()

    startServerThread()
    startRoutinedThread()
    startSyncThread()