import os
import json

from collections import namedtuple

from queue import Queue

from carrot.model import CarrotModel, InstalledModModel, BaseModModel
from carrot.backend import BackendService
from carrot.colors import *


MODS_FILE_NAME = 'mods.json'


FetchRequest = namedtuple('FetchRequest', ['mod_key', 'mc_version', 'channel', 'dependency'])
InstallRequest = namedtuple('InstallRequest', ['mod_info', 'dependency'])


class CarrotService:
    def __init__(self):
        self.backend = BackendService()
    
    def read_carrot(self):
        if os.path.exists(MODS_FILE_NAME):
            with open(MODS_FILE_NAME, 'r') as cf:
                data = json.loads(cf.read())
                carrot = CarrotModel.from_dict(data)
                return carrot

    def save_carrot(self, carrot: CarrotModel):
        with open(MODS_FILE_NAME, 'w+') as cf:
            data = carrot.to_dict()
            cf.write(json.dumps(data, indent=4))
    
    def initialized(self):
        carrot = self.read_carrot()
        return carrot is not None

    def initialize(self, data: dict):
        config = CarrotModel.from_dict(data)
        d = config.to_dict()

        with open(MODS_FILE_NAME, 'w+') as cf:
            cf.write(json.dumps(d, indent=True))
    
    def install(self, mod_key: str):
        carrot = self.read_carrot()
        if not carrot:
            print('Mod repo not initialized. Use "carrot init".')
            return

        # TODO: Test if already installed
        
        mods = self.backend.search_by_mod_key(mod_key, carrot.mc_version)
        
        if not mods:
            print('No matches found, please verify mod key specified or use "carrot search" to find a mod to install.')
            return

        exact_match = find_mod_by_key(mods, mod_key)

        if exact_match:
            print('Found exact match')

            im = InstallationManager()
            im.queue_fetch(FetchRequest(
                mod_key=mod_key,
                mc_version=carrot.mc_version,
                channel=carrot.channel, # TODO: Override via option
                dependency=False
            ))
            im.run(carrot)

            self.save_carrot(carrot)

        else:
            print(f'No mod found in top downloaded mods matching exactly the key "{mod_key}". These are the top downloaded matches:')
            for mod in mods:
                print(f'{colorify(mod.key, WHITE+BRIGHT)} {colorify(mod.name, YELLOW+BRIGHT)} by {colorify(mod.owner, GREEN+BRIGHT)}')
                print(f'\t{colorify(mod.blurb, WHITE)}')
                if mod.categories:
                    print('\t' + ', '.join([f'{colorify(c, BLUE+BRIGHT)}' for c in mod.categories]))


class InstallationManager:
    def __init__(self):
        self.backend = BackendService()

        self.fetch_q = Queue()
        self.install_q = Queue()

    def queue_fetch(self, request: FetchRequest):
        self.fetch_q.put(item=request)

    def run(self, carrot: CarrotModel):
        while not self.fetch_q.empty():
            req = self.fetch_q.get()

            mod = self.backend.get_mod_info(req.mod_key)

            if req.dependency:
                print(f'Fetching mod {colorify(mod.key, WHITE+BRIGHT)} as dependency...')
            else:
                print(f'Fetching mod {colorify(mod.key, WHITE+BRIGHT)}...')

            mod.file = self.backend.get_newest_file_info(req.mod_key, req.mc_version, req.channel)

            # TODO: Do it more cleverly - no need to d/l a file if we will not update it
            file_contents = self.backend.download_file(mod.file.download_url)
            self.put_file_in_cache(file_contents, mod.file.file_name)

            self.install_q.put(InstallRequest(
                mod_info=mod,
                dependency=req.dependency
            ))

            for dep in mod.file.mod_dependencies:
                self.queue_fetch(FetchRequest(
                    mod_key=dep,
                    mc_version=req.mc_version,
                    channel=req.channel,
                    dependency=True
                ))

        print('Fetch phase complete. Proceeding to installation...')

        while not self.install_q.empty():
            req = self.install_q.get()

            current_mod = find_mod_by_key(carrot.mods, req.mod_info.key)
            new_mod = InstalledModModel.from_dict(req.mod_info.to_dict())

            if not current_mod:
                # Installing a completely new mod
                print(f'Installing mod {colorify(req.mod_info.name, WHITE + BRIGHT)} with file {colorify(req.mod_info.file.file_name, RED)}...')
                carrot.mods.append(new_mod)

                self.move_file_from_cache_to_content(new_mod.file.file_name)

            elif current_mod.file.id < req.mod_info.file.id:
                # Updating an already installed mod
                # TODO: Should this be the default behaviour?
                print(f'Updating mod {colorify(req.mod_info.name, WHITE + BRIGHT)} with newer file {colorify(req.mod_info.file.file_name, RED)}...')

                # TODO: Check/update dependency status
                replace_mod_by_key(carrot.mods, req.mod_info.key, new_mod)

                self.delete_file(current_mod.file.file_name)
                self.move_file_from_cache_to_content(req.mod_info.file.file_name)

            elif current_mod.file.id == req.mod_info.file.id:
                # Already at newest version
                # TODO: What if the downloaded file is older because of channel override?
                print(f'Skipping mod {colorify(req.mod_info.name, WHITE + BRIGHT)} due to file {colorify(req.mod_info.file.file_name, RED)} being up to date.')

                # TODO: Do check/update, however the dependency status

            else:
                # Not yet possible, TODO: resolve when channel override becomes a thing
                print('The impossible happened! An older file was downloaded for mod {colorify(req.mod_info.name, WHITE + BRIGHT)}!')
                raise NotImplementedError

        print('Installation phase complete.')

    def put_file_in_cache(self, content: bytes, file_name: str):
        if not os.path.exists('.carrot_cache'):
            os.mkdir('.carrot_cache')

        with open('.carrot_cache/' + file_name, 'wb+') as f:
            f.write(content)

    def delete_file(self, file_name: str):
        os.remove(file_name)

    def move_file_from_cache_to_content(self, file_name: str):
        os.rename('.carrot_cache/' + file_name, file_name)


def find_mod_by_key(mods: list, mod_key: str):
    try:
        return next((m for m in mods if m.key == mod_key))
    except StopIteration:
        return None

def replace_mod_by_key(mods: list, mod_key: str, replacement: BaseModModel):
    for i, mod in enumerate(mods):
        if mod.key == mod_key:
            mods[i] = replacement
            return