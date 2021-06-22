import file_manager


def queryRouter(query):
    if(len(query) == 0):
        return 


def locationRouter(location):
    fileInfo = file_manager.getFile(location)
    return fileInfo


def entry(query, location):
    print(query, location)
    queryRouterRes = queryRouter(query)

    if(queryRouterRes is None):
        print("no queries")

    fileInfo = locationRouter(location)
    return fileInfo