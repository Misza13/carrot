import requests

from carrot_mc import meta
from carrot_mc.model import ModModel, ModFileModel

API_ENDPOINT = 'https://api.carrot-mc.xyz/prod/'


class BackendService:
    def search_by_mod_key(self, mod_key: str, mc_version: str) -> list:
        r = requests.get(
            url=f'{API_ENDPOINT}mods?mc_version={mc_version}&mod_key={mod_key}&page_size=30',
            headers=self._get_default_headers()
        )
        mods = [ModModel.from_dict(m) for m in r.json()['result']]
        return mods

    def get_mod_info(self, mod_key: str) -> ModModel:
        r = requests.get(
            url=f'{API_ENDPOINT}mod/{mod_key}',
            headers=self._get_default_headers()
        )
        mod = ModModel.from_dict(r.json()['result'])
        return mod

    def get_newest_file_info(self, mod_key: str, mc_version: str, channel: str) -> ModFileModel:
        r = requests.get(
            url=f'{API_ENDPOINT}mod/{mod_key}/files?mc_version={mc_version}&channel={channel}&newest_only=1',
            headers=self._get_default_headers()
        )
        result = r.json()['result']
        if result:
            file = ModFileModel.from_dict(result[0])
            return file

    def download_file(self, download_url: str) -> bytes:
        r = requests.get(
            url=download_url,
            headers=self._get_default_headers()
        )
        result = r.content
        return result

    def _get_default_headers(self):
        return {
            'User-Agent': 'Carrot ' + meta.VERSION
        }