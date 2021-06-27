

def getNewStorageItem():
    return dict(
        routined = dict(
            events = [
                dict(                    
                    name="Day",
                    timeInMin = 380,
                    color = "eaf6fb",
                    brightness = 90
                ),                
                dict(                    
                    name="Evening",
                    timeInMin = 1230,
                    color = "ebb63e",
                    brightness = 10
                )
            ],
            lamps = ["65546"]
        )
    )

def createDevice(id, name):
    return dict(
        id=id,
        name=name,
    )


