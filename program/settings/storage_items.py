
def getNewStorageItem():
    return dict(
        endpoint = "",
        events = [
            dict(                 
                name="Day",
                timeInMin = 380,
                timeStr = "6:00",
                actions = [
                    dict(
                        action = "setBrightess"
                    )
                ],
                color = "eaf6fb",
                brightness = 90,
                lamps = ["65546"]
            )
        ]
    )

