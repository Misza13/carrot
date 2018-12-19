import os
import json

from carrot.model import CarrotConfiguration

MODS_FILE_NAME = 'mods.json'


class Carrot:
    def initialized(self):
        #TODO: Check more things, e.g. the validity of the file
        if os.path.exists(MODS_FILE_NAME):
            return True
        else:
            return False

    def initialize(self, name, mc_version, channel):
        config = CarrotConfiguration(name, mc_version, channel)
        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(json.dumps(config.to_object(), indent=True))
