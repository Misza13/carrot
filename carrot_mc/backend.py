import requests

from carrot_mc.model import ModModel, ModFileModel

API_ENDPOINT = 'https://ddph1n5l22.execute-api.eu-central-1.amazonaws.com/dev/'


class BackendService:
    def search_by_mod_key(self, mod_key: str, mc_version: str) -> list:
        r = requests.get(url=f'{API_ENDPOINT}mods?mc_version={mc_version}&mod_key={mod_key}&page_size=30')
        mods = [ModModel.from_dict(m) for m in r.json()['result']]
        return mods

    def get_mod_info(self, mod_key: str) -> ModModel:
        r = requests.get(url=f'{API_ENDPOINT}mod/{mod_key}')
        mod = ModModel.from_dict(r.json()['result'])
        return mod

    def get_newest_file_info(self, mod_key: str, mc_version: str, channel: str) -> ModFileModel:
        r = requests.get(url=f'{API_ENDPOINT}mod/{mod_key}/files?mc_version={mc_version}&channel={channel}&newest_only=1')
        result = r.json()['result']
        if result:
            file = ModFileModel.from_dict(result[0])
            return file

    def download_file(self, download_url: str) -> bytes:
        r = requests.get(url=download_url)
        result = r.content
        return result