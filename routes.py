import storage_handler
import response_file_manager
import tradfri_handler
import json


#ANCHOR jsons
def allSafeStorageParameters():
    safeStorageContentJson = storage_handler.getSafeStorageContentJson()
    return dict(resCode = 200, mimeType="text/json", fileContent=safeStorageContentJson.encode('utf-8'))

def indexJson():
    contentDict = dict(isSetup = tradfri_handler.isSetup)
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def lampPickerJson():
    contentDict = dict(devices = tradfri_handler.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)


specialRoutes = dict(
    allSafeStorageParameters=allSafeStorageParameters,
    indexJson=indexJson
)


def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName

def getspecialRouteFileDict(location):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute()
    return newLocation

