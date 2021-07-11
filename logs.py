logsList = list(["====logs first item===="])

def getLogs():
    return logsList

def addLog(*logInput):
    logStr = ""
    for log in logInput:
        logStr += str(log) + " "
    logsList.append(logStr)
    print("log:", logStr)