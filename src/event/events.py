class Events:
    events = []
    _updateListener = []


    #========== CONSTRUCTOR ==========

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Events, cls).__new__(cls)

        return cls.instance



    def setEvents(self, events):
        self.events = events


    #========== LISTENERS ==========

    def addUpdateListener(self, storageUpdateListener):
        self._updateListener.append(storageUpdateListener)

    def callOnUpdateListeners(self):
        for listener in self._updateListener:
            listener()

