from datetime import datetime
import asyncio
import os


# ========= SETUP =========

def _getLogFilePath():
    LOG_FILE_NAME = ".log"
    parentFolderName = os.path.dirname(os.path.realpath(__file__))
    logFolder = os.path.dirname(parentFolderName)
    return logFolder + os.path.sep + LOG_FILE_NAME

_LOG_PATH = _getLogFilePath()


def getLogs() -> list:
    if not os.path.exists(_LOG_PATH):
        return ""

    logs = []
    with open(_LOG_PATH, "r") as f:
        for line in f:
            logs.append(line)

    return logs



def log(*logInput):
    logStr = _createLogStr(logInput)
    print("log:", logStr, flush=True)
    asyncio.run(_saveLog(logStr))


def _createLogStr(logInput):
    logStr = f"{str(datetime.now())}: "
    for log in logInput:
        logStr += str(log) + " "
    return logStr


async def _saveLog(log):
    with open(_LOG_PATH, "a+") as myfile:
        myfile.write(f"{log}\n")


# Initial message
asyncio.run(_saveLog(f"\n\n============ STARTED AT {str(datetime.now())} =============\n"))