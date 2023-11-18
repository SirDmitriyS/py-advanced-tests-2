import json
import os

import requests


def load_token():
    if os.path.exists('config.txt'):
        with open('config.txt', 'rt') as config_file:
            config = json.load(config_file)
            ya_token = config.get('ya token')
    return ya_token

class YaDiskApi:

    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token
    
    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        return headers
    
    def create_dir(self, name, path = '/'):
        res = requests.put(
            url=self.url + 'resources',
            params={'path': f'{path.rstrip("/")}/{name}'},
            headers=self.get_headers()
        )
        return res.status_code

    def get_dir(self, name, path = '/'):
        res = requests.get(
            url=self.url + 'resources',
            params={'path': f'{path.rstrip("/")}/{name}', 'fields': 'name'},
            headers=self.get_headers(),
        )
        return res.json()

if __name__ == '__main__':
    token = load_token()

    ya_disk_api = YaDiskApi(token)

    res = ya_disk_api.create_dir('test')
    print(res)

    res = ya_disk_api.get_dir('test')
    print(res)