from carrot_mc.colors import Colorizer as clr

class CliEventPrinter:
    def handle(self, event: str, payload=None):
        method_name = 'handle_' + event.replace(' ', '_')
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(payload)

    def handle_info(self, payload):
        print(payload)

    def handle_match_list(self, payload):
        print(f'No mod found in top downloaded mods matching exactly the key "{clr.mod_key(payload.mod_key)}". These are the top downloaded matches:')
        for mod in payload.mods:
            print(f'[{clr.mod_key(mod.key)}] {clr.mod_name(mod.name)} by {clr.mod_owner(mod.owner)}')
            print(f'\t{clr.mod_blurb(mod.blurb)}')
            if mod.categories:
                print('\t' + ', '.join([f'{clr.mod_category(c)}' for c in mod.categories]))

    def handle_mod_enabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} enabled.')

    def handle_mod_disabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} disabled.')

    def handle_warn_mod_already_enabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is already enabled.')

    def handle_warn_mod_already_disabled(self, payload):
        print(f'Mod {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is already disabled.')

    def handle_error_no_repo(self, payload):
        print(clr.error(f'Mod repo not initialized. Use "{clr.cli("carrot init")}".'))

    def handle_error_no_mod_key_match(self, payload):
        print(f'No matches found, please verify mod key specified or use "{clr.cli("carrot search")}" to find a mod to install.')

    def handle_error_mod_not_installed(self, payload):
        print(f'No mod matching exactly the key "{clr.mod_key(payload.mod_key)}" is currently installed.')

    def handle_error_no_mods_installed(self, payload):
        print(f'No mods are installed. Use "{clr.cli("carrot install")}" to install some.')

    def handle_error_mod_file_missing(self, payload):
        print(f'Mod file for {clr.mod_name(payload.mod.name)} {clr.mod_key("[" + payload.mod.key + "]")} is {clr.error("missing")}.')