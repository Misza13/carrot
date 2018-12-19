import os
import json

MODS_FILE_NAME = 'mods.json'


class Carrot:
    def initialized(self):
        #TODO: Check more things, e.g. the validity of the file
        if os.path.exists(MODS_FILE_NAME):
            return True
        else:
            return False

    def initialize(self):
        config = CarrotConfiguration()
        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(config.to_json())


class CarrotConfiguration:
    def to_json(self):
        return '{}'