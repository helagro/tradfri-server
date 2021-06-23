import storage_handler
import response_file_manager
import tradfriHandler
import json


def allSafeStorageParameters():
    safeStorageContentJson = storage_handler.getSafeStorageContentJson()
    return dict(resCode = 200, mimeType="text/json", fileContent=safeStorageContentJson.encode('utf-8'))


def isTradfriSetup():
    contentDict = dict(isSetup = tradfriHandler.isSetup)
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)


def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName


specialRoutes = dict(
    allSafeStorageParameters=allSafeStorageParameters,
    isTradfriSetup=isTradfriSetup
)

def getspecialRouteFileDict(location):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute()
    return newLocation

