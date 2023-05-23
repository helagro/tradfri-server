from http.server import HTTPServer
import threading
from server.server import MyServer
import event.event_schedule as event_schedule
import argparse
import logger
from event import sync


def _main():
    noDownloads = _parseArguments()
    if not noDownloads: sync.sync()

    _startServerThread()
    _startRoutinedThread()
    _startSyncThread()
    

def _parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--noDownload", action="store_true")
    args = parser.parse_args()

    if args.noDownload: logger.log("will not download events")

    return args.noDownload



def _startServerThread():
    t = threading.Thread(target=_startServer)
    t.start()

def _startServer():
    httpd = HTTPServer(('0.0.0.0', 8000), MyServer)
    httpd.serve_forever()


def _startRoutinedThread():
    t = threading.Thread(target=event_schedule.start)
    t.start()


def _startSyncThread():
    t = threading.Thread(target=sync.scheduleSync)
    t.start()



if __name__ == "__main__":
    _main()