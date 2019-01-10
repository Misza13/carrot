import os
import json
import hashlib

from collections import namedtuple

from queue import Queue

from carrot_mc.model import CarrotModel, InstalledModModel, BaseModModel
from carrot_mc.backend import BackendService
from carrot_mc.colors import Colorizer as clr
from carrot_mc.meta import VERSION


MODS_FILE_NAME = 'mods.json'


FetchRequest = namedtuple('FetchRequest', ['mod_key', 'mc_version', 'channel', 'dependency'])
DownloadRequest = namedtuple('DownloadRequest', ['mod_info', 'dependency'])
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
        carrot.carrot_version = VERSION
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
    
    def status(self, args):
        carrot = self.read_carrot()
        
        dep_count = 0
        disabled_count = 0
        missing_file_err = []
        bad_md5_err = []
        
        for mod in carrot.mods:
            if mod.dependency:
                dep_count += 1
            
            actual_file_name = None
            if os.path.exists(mod.file.file_name):
                actual_file_name = mod.file.file_name
            elif os.path.exists(mod.file.file_name + '.disabled'):
                disabled_count += 1
                actual_file_name = mod.file.file_name + '.disabled'
            
            if not actual_file_name:
                missing_file_err.append(mod)
            else:
                file_contents = open(actual_file_name, 'rb').read()
                
                md5 = hashlib.md5()
                md5.update(file_contents)
                
                if md5.hexdigest() != mod.file.file_md5:
                    bad_md5_err.append((mod, actual_file_name, md5.hexdigest()))
        
        print(f'Mods installed: {len(carrot.mods)}')
        
        if dep_count:
            print(f'of which dependencies: {dep_count}')
        
        if disabled_count > 0:
            print(f'Disabled mod(s): {disabled_count}')
        
        if len(missing_file_err) + len(bad_md5_err) == 0:
            print('All mod files seem to be in order.')
        else:
            if missing_file_err:
                print(f'{len(missing_file_err)} mod(s) have missing files:')
                for mod in missing_file_err:
                    print(f'\t{clr.mod_name(mod.name)}: missing file {clr.file_name(mod.file.file_name)}')
        
            if bad_md5_err:
                print(f'{len(bad_md5_err)} mod(s) have possibly corrupted files:')
                for mod, actual_file_name, actual_md5 in bad_md5_err:
                    print(f'\t{clr.mod_name(mod.name)}: file {clr.file_name(actual_file_name)} has hash {clr.file_hash(actual_md5)} instead of {clr.file_hash(mod.file.file_md5)}')
                
    
    def install(self, args):
        carrot = self.read_carrot()
        if not carrot:
            print('Mod repo not initialized. Use "carrot init".')
            return

        if args.channel:
            channel = args.channel
        else:
            channel = carrot.channel

        im = InstallationManager()

        if len(args.mod_key) > 1:
            for mod_key in args.mod_key:
                im.queue_fetch(FetchRequest(
                    mod_key=mod_key,
                    mc_version=carrot.mc_version,
                    channel=channel,
                    dependency=False
                ))

        else:
            mod_key = args.mod_key[0]
            mods = self.backend.search_by_mod_key(mod_key, carrot.mc_version)

            if not mods:
                print('No matches found, please verify mod key specified or use "carrot search" to find a mod to install.')
                return

            exact_match = find_mod_by_key(mods, mod_key)

            if exact_match:
                print('Found exact match')

                im.queue_fetch(FetchRequest(
                    mod_key=mod_key,
                    mc_version=carrot.mc_version,
                    channel=channel,
                    dependency=False
                ))

            else:
                print(f'No mod found in top downloaded mods matching exactly the key "{clr.mod_key(mod_key)}". These are the top downloaded matches:')
                for mod in mods:
                    print(f'[{clr.mod_key(mod.key)}] {clr.mod_name(mod.name)} by {clr.mod_owner(mod.owner)}')
                    print(f'\t{clr.mod_blurb(mod.blurb)}')
                    if mod.categories:
                        print('\t' + ', '.join([f'{clr.mod_category(c)}' for c in mod.categories]))
                return

        im.run(carrot, args)

        self.save_carrot(carrot)


    def update(self, args):
        carrot = self.read_carrot()
        if not carrot:
            print('Mod repo not initialized. Use "carrot init".')
            return

        im = InstallationManager()

        if args.mod_key:
            local_mod = find_mod_by_key(carrot.mods, args.mod_key)

            if not local_mod:
                print(f'No mod matching exactly the key "{clr.mod_key(args.mod_key)}" is currently installed.')
                return

            if args.channel:
                channel = args.channel
            else:
                channel = local_mod.file.release_type

            im.queue_fetch(FetchRequest(
                mod_key=args.mod_key,
                mc_version=carrot.mc_version,
                channel=channel,
                dependency=local_mod.dependency
            ))

        else:
            if not carrot.mods:
                print(f'No mods are installed. Use "{clr.cli("carrot install")}" to install some.')
                return

            for mod in carrot.mods:
                if args.channel:
                    channel = args.channel
                else:
                    channel = mod.file.release_type

                if not mod.dependency:
                    im.queue_fetch(FetchRequest(
                        mod_key=mod.key,
                        mc_version=carrot.mc_version,
                        channel=channel,
                        dependency=False
                    ))
                    # TODO: How to purge dependencies that are no longer valid?

        im.run(carrot, args)
        self.save_carrot(carrot)


class InstallationManager:
    def __init__(self):
        self.backend = BackendService()

        self.fetch_q = Queue()
        self.download_q = Queue()
        self.install_q = Queue()

        self._download_hist = set()
        self._install_hist = set()

    def queue_fetch(self, request: FetchRequest):
        self.fetch_q.put(item=request)

    def queue_download(self, request: DownloadRequest):
        self.download_q.put(item=request)

    def queue_install(self, request: InstallRequest):
        self.install_q.put(item=request)

    def run(self, carrot: CarrotModel, args):
        while not self.fetch_q.empty():
            req = self.fetch_q.get()
            self.do_fetch(req, carrot, args)

        print('Mod check phase complete. Proceeding to download...')

        while not self.download_q.empty():
            req = self.download_q.get()
            self.do_download(req, carrot, args)

        print('Download phase complete. Proceeding to installation...')

        while not self.install_q.empty():
            req = self.install_q.get()
            self.do_install(req, carrot, args)

        print('Installation phase complete.')

    def do_fetch(self, req: FetchRequest, carrot: CarrotModel, args):
        print(f'Checking mod {clr.mod_key(str(req.mod_key))}...', end=' ')

        mod_info = self.backend.get_mod_info(req.mod_key)

        if not mod_info.key:
            print(clr.error('Not found!'))
            return

        print(f'{clr.mod_name(mod_info.name)}...', end=' ')

        mod_info.file = self.backend.get_newest_file_info(req.mod_key, req.mc_version, req.channel)

        current_mod = find_mod_by_key(carrot.mods, mod_info.key)

        if not mod_info.file:
            print('Mod has no files in the chosen channel. Skipping.', end=' ')
            
            proceed = False

        elif not current_mod:
            print('New mod.', end=' ')

            proceed = True

        elif current_mod.file.id < mod_info.file.id:
            if args.upgrade:
                print('Mod already installed, found new version and will upgrade because it\'s allowed.',
                      end=' ')

                proceed = True

            else:
                print(f'A newer file was found but upgrades are disabled by default. Use the {clr.cli("--upgrade")} option if this should be allowed.',
                      end=' ')

                if req.dependency:
                    print(f'\n{clr.emph("NOTE")}: Because this is a dependency, it will {clr.emph("not")} be re-checked if you re-run last install command. Use "{clr.cli("carrot update " + mod_info.key)}" to do it explicitly.',
                          end=' ')

                proceed = False

        elif current_mod.file.id == mod_info.file.id:
            print('Already at newest version.',
                  end=' ')

            proceed = False

        else:
            if args.downgrade:
                print('Mod already installed, found older version and will downgrade because it\'s allowed.',
                      end=' ')

                proceed = True
            else:
                print(f'An older file was found but downgrades are disabled by default. Use the {clr.cli("--downgrade")} option if this was intended.',
                      end=' ')

                proceed = False

        if proceed:
            self.download_q.put(DownloadRequest(
                mod_info=mod_info,
                dependency=req.dependency
            ))

            self.install_q.put(InstallRequest(
                mod_info=mod_info,
                dependency=req.dependency
            ))

            if mod_info.file.mod_dependencies:
                print('Detected dependencies.', end=' ')

                for dep in mod_info.file.mod_dependencies:
                    self.queue_fetch(FetchRequest(
                        mod_key=dep,
                        mc_version=req.mc_version,
                        channel=req.channel,
                        dependency=True
                    ))

        print('')

    def do_download(self, req: DownloadRequest, carrot: CarrotModel, args):
        if req.mod_info.file.file_name in self._download_hist:
            return

        print(f'Downloading file {clr.file_name(req.mod_info.file.file_name)} from {clr.url(req.mod_info.file.download_url)}...')
        file_contents = self.backend.download_file(req.mod_info.file.download_url)
        self.put_file_in_cache(file_contents, req.mod_info.file.file_name)
        self._download_hist.add(req.mod_info.file.file_name)

    def do_install(self, req: InstallRequest, carrot: CarrotModel, args):
        if req.mod_info.file.file_name in self._install_hist:
            return

        current_mod = find_mod_by_key(carrot.mods, req.mod_info.key)
        new_mod = InstalledModModel.from_dict(req.mod_info.to_dict())
        new_mod.dependency = req.dependency

        if not current_mod:
            print(f'Installing mod {clr.mod_name(req.mod_info.name)} with file {clr.file_name(req.mod_info.file.file_name)}...')
            carrot.mods.append(new_mod)

            self.move_file_from_cache_to_content(new_mod.file.file_name)

        else:
            print(f'Updating mod {clr.mod_name(req.mod_info.name)}...', end=' ')

            # Prevent a user-installed mod from becoming a dependency
            if not current_mod.dependency and new_mod.dependency:
                new_mod.dependency = False

            replace_mod_by_key(carrot.mods, req.mod_info.key, new_mod)

            enabled = self.delete_file(current_mod.file.file_name)
            if enabled:
                print(f'Installing new file {clr.file_name(req.mod_info.file.file_name)}...', end=' ')
            else:
                print(f'Installing new file {clr.file_name(req.mod_info.file.file_name + ".disabled")} because current file was also {clr.file_name(".disabled")}...', end=' ')
            self.move_file_from_cache_to_content(req.mod_info.file.file_name, enabled)
            
            print('')

        self._install_hist.add(req.mod_info.file.file_name)

    def put_file_in_cache(self, content: bytes, file_name: str):
        if not os.path.exists('.carrot_cache'):
            os.mkdir('.carrot_cache')

        with open('.carrot_cache/' + file_name, 'wb+') as f:
            f.write(content)

    def delete_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)
            return True
            
        elif os.path.exists(file_name + '.disabled'):
            os.remove(file_name + '.disabled')
            return False
        
        # If file is missing, assume it's meant to be installed and enabled
        return True

    def move_file_from_cache_to_content(self, file_name: str, enabled: bool = True):
        target_file_name = file_name
        if not enabled:
            target_file_name += '.disabled'
        
        os.rename('.carrot_cache/' + file_name, target_file_name)


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