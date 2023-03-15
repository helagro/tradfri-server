class Events:
    events = []


    #========== CONSTRUCTOR ==========

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Events, cls).__new__(cls)
            cls.instance.loadSettings()
        return cls.instance


    #========== LISTENERS ==========

    def addStorageUpdateListener(self, storageUpdateListener):
        self.storageContentUpdateListeners.append(storageUpdateListener)

    def callOnUpdateListeners(self):
        for listener in self.storageContentUpdateListeners:
            listener()

