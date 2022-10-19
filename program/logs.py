from datetime import datetime

logsList = list([])

def getLogs():
    return logsList

def log(*logInput):
    logStr = createLogStr(logInput)
    logsList.append(logStr)
    print("log:", logStr, flush=True)

    if len(logsList) > 100:
        logsList.pop(0)

def createLogStr(logInput):
    logStr = str(datetime.now())
    logStr += "\n"
    for log in logInput:
        logStr += str(log) + " "
    return logStr