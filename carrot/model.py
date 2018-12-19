
class CarrotConfiguration:
    def __init__(self, name, mc_version, channel):
        self.version = 1
        self.name = name
        self.mc_version = mc_version
        self.channel = channel

    def to_object(self):
        return {
            'version': self.version,
            'name': self.name,
            'mc_version': self.mc_version,
            'channel': self.channel
        }