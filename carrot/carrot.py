import os
import json

from carrot.model import CarrotModel
from carrot.backend import BackendService

MODS_FILE_NAME = 'mods.json'


class CarrotService:
    backend = BackendService()
    
    def read_mods_file(self):
        if os.path.exists(MODS_FILE_NAME):
            with open(MODS_FILE_NAME, 'r') as cf:
                data = json.loads(cf.read())
                carrot = CarrotModel.from_dict(data)
                return carrot

        return None
    
    def initialized(self):
        carrot = self.read_mods_file()
        return carrot is not None

    def initialize(self, data):
        config = CarrotModel.from_dict(data)
        d = config.to_dict()

        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(json.dumps(d, indent=True))
    
    def install(self, mod_key):
        carrot = self.read_mods_file()
        if not carrot:
            print('Mod repo not initialized. Use "carrot init".')
            return
        
        mods = self.backend.search_by_mod_key(mod_key, carrot.mc_version)
        
        if not mods:
            print('No matches found, please verify mod key specified or use "carrot search" to find a mod to install.')
            return
        
        try:
            exact_match = next((m for m in mods if m.key == mod_key))
        except StopIteration:
            exact_match = None
        
        if exact_match:
            print('Found exact match')
            #TODO: Perform installation
        else:
            print(f'No mod found in top downloaded mods matching exactly the key "{mod_key}". These are the top downloaded matches:')
            for mod in mods:
                print(f'{color_seq(WHITE+BRIGHT)}[{mod.key}]{RESET} {color_seq(YELLOW+BRIGHT)}{mod.name}{RESET} by {color_seq(GREEN+BRIGHT)}{mod.owner}{RESET}')
                print(f'\t{color_seq(WHITE)}{mod.blurb}{RESET}')
                if mod.categories:
                    print('\t' + ', '.join([f'{color_seq(BLUE+BRIGHT)}{c}{RESET}' for c in mod.categories]))



#TODO: Refactor below into separate file
BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

BRIGHT = 8

RESET = '\x1b[0m'

def color_seq(color):
    if color & BRIGHT:
        return f'\x1b[{(color & 7) + 30};1m'
    else:
        return f'\x1b[{(color & 7) + 30}m'

def colorify(text, color):
    return color_seq(color) + text + RESET