from datetime import datetime

def getLogs():
    f = open(".log", "f")
    logs = f.read()
    f.close()
    return logs

def log(*logInput):
    logStr = createLogStr(logInput)
    print("log:", logStr, flush=True)
    saveLog(logStr)


def createLogStr(logInput):
    logStr = f"{str(datetime.now())}: "
    for log in logInput:
        logStr += str(log) + " "
    return logStr


async def saveLog(log):
    with open(".log", "a") as myfile:
        myfile.write(log)