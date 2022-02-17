import response_file_manager
import routes


def locationRouter(location, query):
    specialRouteFileDict = routes.getspecialRouteFileDict(location, query)
    if(not specialRouteFileDict is None):
        return specialRouteFileDict


    return response_file_manager.getFile(location)


def entry(query, location):
    fileInfo = locationRouter(location, query)
    return fileInfo