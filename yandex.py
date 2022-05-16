import requests
from pprint import pp, pprint


class YaUploader:
    host = 'https://cloud-api.yandex.net'
    def __init__(self, token):
        self.token = token

    def creating_a_folder(self, path):
        url = f"{self.host}/v1/disk/resources/"
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.put(url, params=params, headers=headers)
        pprint(response.json())
        return response.json().get('href')

    def upload_from_url(self, path, file_url):
        url = f"{self.host}/v1/disk/resources/upload/"
        headers = self.get_headers()
        params = {'path': path, 'url': file_url, 'overwrite': True}
        response = requests.post(url, params=params, headers=headers)
        pprint(f"Status: {response.status_code}")
        if response.status_code == 202:
            print('the file is uploaded!')
        return response.json().get('href')

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f"OAuth {self.token}"}

    def _get_upload_link(self, path):
        url = f"{self.host}/v1/disk/resources/upload/"
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, params=params, headers=headers)
        pprint(response.json())
        return response.json().get('href')

    def upload_file(self, path, file_list):
        for file_name in file_list:
            upload_link = self._get_upload_link(path)
            headers = self.get_headers()
            response = requests.put(upload_link, data=open(file_name, 'rb'), headers=headers)
            response.raise_for_status()
            if response.status_code == 201:
                print('the file is uploaded!')
