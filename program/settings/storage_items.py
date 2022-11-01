
def getNewStorageItem():
    return dict(
        endpoint = "https://hook.eu1.make.com/",
        events = [
            dict(                 
                name="wake up",
                timeInMin = 380,
                timeStr = "6:00",
                actions = [
                    dict(
                        name = "setBrightessLevel",
                        payload = "150",
                        device = "65546"
                    )
                ],
            )
        ]
    )

