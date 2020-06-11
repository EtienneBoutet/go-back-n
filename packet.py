class DataPacket:
    def __init__(self, data, lastPck, isLast):
        self.data = data
        self.lastPck = lastPck
        self.isLast = isLast

class RequestPacket:
    def __init__(self, mode):
        self.mode = mode
