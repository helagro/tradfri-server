import storage_handler
import response_file_manager
import tradfri_handler
import json


#ANCHOR jsons
def allSafeStorageParameters():
    safeStorageContentJson = storage_handler.getStorageContent()
    return dict(resCode = 200, mimeType="text/json", fileContent=safeStorageContentJson.encode('utf-8'))

def lampPickerJson():
    contentDict = dict(devices = tradfri_handler.getDevices())
    contentDictStr = json.dumps(contentDict)
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)

def deviceControlJson(query):
    deviceId = json.loads(query["device"][0])["id"]
    action = query["action"][0]
    print("deviceId", deviceId, "action", action)
    tradfri_handler.performAction(deviceId, action)
    contentDictStr = "what is that"
    fileContent = contentDictStr.encode('utf-8')
    return dict(resCode = 200, mimeType="text/json", fileContent=fileContent)



specialRoutes = dict(
    allSafeStorageParameters=allSafeStorageParameters,
    lampPickerJson=lampPickerJson,
    deviceControlJson=deviceControlJson  
)


def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName

def getspecialRouteFileDict(location, query):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute(query)
    return newLocation

