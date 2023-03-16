from datetime import datetime
import asyncio
import os


def getLogFilePath():
    logFileName = ".log"
    parentFolderName = os.path.dirname(os.path.realpath(__file__))
    logFolder = os.path.dirname(parentFolderName)
    return logFolder + os.path.sep + logFileName

LOG_PATH = getLogFilePath()

def getLogs():
    if not os.path.exists(LOG_PATH):
        return ""

    logs = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            logs.append(line)

    return logs

def log(*logInput):
    logStr = createLogStr(logInput)
    print("log:", logStr, flush=True)
    asyncio.run(saveLog(logStr))


def createLogStr(logInput):
    logStr = f"{str(datetime.now())}: "
    for log in logInput:
        logStr += str(log) + " "
    return logStr


async def saveLog(log):
    with open(LOG_PATH, "a+") as myfile:
        myfile.write(f"{log}\n")


asyncio.run(saveLog(f"\n\n============ STARTED AT {str(datetime.now())} =============\n"))