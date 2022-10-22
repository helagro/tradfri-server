from . import routes_files
from . import routes_special

def route(location: str, query: dict):
    hasOtherRoute = routes_special.hasRoute(location)

    if(hasOtherRoute):
        return routes_special.getspecialRouteFileDict(location, query)
    else:
        return routes_files.getFile(location)