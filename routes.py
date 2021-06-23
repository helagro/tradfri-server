import storage_handler
import response_file_manager


def saveStorageForm():
    pass


def allSafeStorageParameters():
    safeStorageContentJson = storage_handler.getSafeStorageContentJson()
    return dict(resCode = 200, mimeType="text/json", fileContent=safeStorageContentJson.encode('utf-8'))


def locationToRouteString(location):
    onlyFileName = location.split("/")[-1]
    return onlyFileName


specialRoutes = dict(
    allSafeStorageParameters=allSafeStorageParameters
)

def getspecialRouteFileDict(location):
    routeString = locationToRouteString(location)

    matchingRoute = specialRoutes.get(routeString, None)

    if(matchingRoute is None):
        return

    newLocation = matchingRoute()
    return newLocation

