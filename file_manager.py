
def getFile(fileName):
    fileStream = open(fileName, "rb")
    fileContent = fileStream.read()
    fileStream.close()
    
    return fileContent