logsList = list(["====logs first item===="])

def getLogs():
    return logsList

def addLog(*logInput):
    logStr = ""
    for log in logInput:
        print("daw", log)
        logStr += str(log) + " "
    print("log:", logStr)
    logsList.append(logStr)