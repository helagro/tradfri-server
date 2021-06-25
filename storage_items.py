

def getNewStorageItem():
    return dict(
        routined = dict(
            events = [
                dict(                    
                    name="Day",
                    device="65546",
                    timeInMin = 380,
                    color = "eaf6fb",
                    brightness = 90
                ),
                dict(                    
                    name="Evening",
                    device="65546",
                    timeInMin = 1230,
                    color = "ebb63e",
                    brightness = 10
                )
            ],
            lamps = []
        )
    )

def createDevice(id, name):
    return dict(
        id=id,
        name=name,
    )


