import requests


class Http:
    def __init__(self, headers):
        self.headers = headers

    def get(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response

    def post(self, url, json_content):
        response = requests.post(url=url, json=json_content, headers=self.headers)
        return response

    def delete(self, url):
        response = requests.delete(url=url, headers=self.headers)
        return response
