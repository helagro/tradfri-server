ITEM_URL_PREFIX_FORMULA = "coaps://$TF_GATEWAYIP:5684/15001"

SUPPORTED_ACTIONS = dict(
    temporaryOn = dict(
        code = "5850",
    ),
    
)

def getNewStorageItem():
    return dict(
        private = dict(
            host = dict(
                identity = None,
                
            ),
            psk_id = None,
            psk = None
        ),
        gatewayIp = None,
        itemUrlPrefix = None,
        devices = dict(),
        actionsData = dict(
            routined = dict(
                actionItems = dict(

                )
            )
        )
    )

def createDevice(id, name):
    return dict(
        id=id,
        name=name,
    )


