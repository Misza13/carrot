import os
import json

from carrot.model import CarrotModel

MODS_FILE_NAME = 'mods.json'


class Carrot:
    def initialized(self):
        if os.path.exists(MODS_FILE_NAME):
            with open(MODS_FILE_NAME, 'r') as cf:
                data = json.loads(cf.read())
                config = CarrotModel.from_dict(data)
                return True

        return False

    def initialize(self, data):
        config = CarrotModel.from_dict(data)
        d = config.to_dict()

        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(json.dumps(d, indent=True))