import json
import requests

from carrot.model import ModModel

API_ENDPOINT = 'https://ddph1n5l22.execute-api.eu-central-1.amazonaws.com/dev/'


class BackendService:
    def search_by_mod_key(self, mod_key, mc_version):
        r = requests.get(url=f'{API_ENDPOINT}mods?mc_version={mc_version}&mod_key={mod_key}&page_size=30')
        mods = [ModModel.from_dict(m) for m in r.json()['result']]
        return mods
