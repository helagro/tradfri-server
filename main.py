from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import env
import random
import threading
from time import sleep
import sys
import subprocess, shlex
from req_handler import SimpleHTTPRequestHandler


def startServer():
    httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def startServerThread():
    t = threading.Thread(target=startServer)
    t.start()


def startRoutined():
    return

def startRoutinedThread():
    t = threading.Thread(target=startRoutined)
    t.start()

if __name__ == "__main__":
    startServerThread()
    startRoutinedThread()
    print("Started successfully")