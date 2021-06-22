from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import env
import random
from threading import Thread, currentThread, Timer
from time import sleep
import sys
import subprocess, shlex
from req_handler import SimpleHTTPRequestHandler


if __name__ == "__main__":
    print("Server started")
    httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()