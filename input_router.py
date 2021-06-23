import response_file_manager
import routes


def queryRouter(query):
    if(len(query) == 0):
        return 


def locationRouter(location):
    specialRouteFileDict = routes.getspecialRouteFileDict(location)
    if(not specialRouteFileDict is None):
        return specialRouteFileDict


    return response_file_manager.getFile(location)


def entry(query, location):
    print(query, location)
    queryRouterRes = queryRouter(query)

    fileInfo = locationRouter(location)
    return fileInfo