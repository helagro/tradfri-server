from datetime import datetime

logsList = list(["====logs start===="])

def getLogs():
    return logsList

def log(*logInput):
    logStr = str(datetime.now())
    logStr += "\n"
    for log in logInput:
        logStr += str(log) + " "
    logsList.append(logStr)
    print("log:", logStr)