from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
import env
import random
from threading import Thread, currentThread, Timer
from time import sleep
import sys
from gpiozero import LED
import subprocess, shlex

IP="192.168.10.239"
DEVICES = {
    "lamp": "15001/65537",
    "desk": "15001/65538",
    "bed": "15001/65539",
    "fan": "15001/65540"
}
COLORS = ["f5faf6","f1e0b5","efd275"]
LEDS = {
    "h": LED(14),
    "o": LED(15),
    "s": LED(18)
}

#essential
def runCommand(payload, target, method="put"):
    command = "coap-client -m %s -u \"%s\" -k \"%s\" -e '%s' \"coaps://%s:5684/%s\"" % (method, env.username, env.preShared, payload, IP, target)
    res = str(subprocess.run(shlex.split(command), stdout=subprocess.PIPE))
    return res


def hasQuerys(wanted, recieved):
    res = {}
    for query in wanted:
        if(query not in recieved):
            return False
        else:
            res[query] = recieved[query][0]
            if(len(res[query]) > 6 or " " in res[query]):
                print("Dangerous input")
                return False
    return res


#specifics
def disco():
    t = currentThread()
    while getattr(t, "do_run", True):
        color = random.choice(COLORS)
        runCommand("{ \"3311\": [{ \"5706\": \"%s\" }] }" % (color), DEVICES["lamp"])
        sleep(10)
tDisco = Thread(target=disco)


#query stages
def act(recieved):
    res = hasQuerys(["act"], recieved)
    if(not res): return ""
    act = res["act"]

    if(act == "0" or act == "1"):
        for key in DEVICES:
            runCommand("{ \"3311\": [{ \"5850\": %s }] }" % act, DEVICES[key])
        return " | Turned %s all devices" % act
    if(act=="quit"):
        sys.exit()
        return " | Quitting program..."
    return ""


def inp(recieved):
    global tDisco

    res = hasQuerys(["act", "inp"], recieved)
    if(not res): return ""
    act = res["act"]
    inp = res["inp"]
    if (act == "disco"):
        if(inp == "1"):
            tDisco = Thread(target=disco)
            tDisco.start()
            return " | Disco started"
        elif(tDisco.is_alive()):
            tDisco.do_run=False
            tDisco.join()
            return " | Disco stopped"

    elif (act == "tOn"):
            lamp = DEVICES[inp]
            runCommand("{ \"3311\": [{ \"5850\": 1}]}", lamp)
            start_time = Timer(3600, runCommand, ["{ \"3311\": [{ \"5850\": 0}]}", lamp])
            start_time.start()
            return " | Temporarly turned on %s" % lamp
    return ""


def usr(recieved):
    res = hasQuerys(["act", "inp", "usr"], recieved)
    if(not res): return ""
    act = res["act"]
    inp = int(res["inp"])
    usr = res["usr"]

    if(usr in [*LEDS]):
        msg = " | Authorized"
        lamp = LEDS[usr]
        if(inp == 1):
            lamp.on()
            msg += " | Turned on %s's lamp" % usr
        else:
            lamp.off()
            msg += " | Turned off %s's lamp" % usr

        if (act == "wL" and usr == "h"):
            if(inp == 1):
                runCommand("{ \"3311\": [{ \"5851\": 254, \"5706\": \"f5faf6\"}] }", DEVICES["lamp"])
            elif (inp == 0):
                runCommand("{ \"3311\": [{ \"5851\": 254, \"5706\": \"f1e0b5\"}] }", DEVICES["lamp"])
            elif (inp == -1):
                runCommand("{ \"3311\": [{ \"5851\": 102, \"5706\": \"efd275\"}] }", DEVICES["lamp"])
            msg += " | Changed DW lighting"
        return msg

    else:
        return " | Invalid user"



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global tDisco
        self.send_response(200)
        self.end_headers()

        recieved = parse.parse_qs(parse.urlsplit(self.path).query)
        print(recieved)

        msg = " | Respose:"
        msg += act(recieved)
        msg += inp(recieved)
        msg += usr(recieved)
        self.wfile.write(msg.encode("utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
