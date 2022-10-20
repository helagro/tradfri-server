import routes_file
import routes_special


def entry(query, location):
    fileInfo = locationRouter(location, query)
    return fileInfo

def locationRouter(location, query):
    hasOtherRoute = routes_special.hasRoute(location)

    if(hasOtherRoute):
        return routes_special.getspecialRouteFileDict(location, query)
    else:
        return routes_file.getFile(location)