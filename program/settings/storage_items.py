

def getNewStorageItem():
    return dict(
        events = [
            dict(                    
                name="Day",
                timeInMin = 380,
                timeStr = "6:00",
                color = "eaf6fb",
                brightness = 90,
                lamps = ["65546"]
            ),                
            dict(                    
                name="Evening",
                timeInMin = 1230,
                timeStr = "20:30",
                color = "ebb63e",
                brightness = 10,
                isSynced = True,
                lamps = ["65546"]
            )
        ],
    )

def createDevice(id, name):
    return dict(
        id=id,
        name=name,
    )


