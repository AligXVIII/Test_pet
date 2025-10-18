import requests


class BaseAPIClient:

    def __init__(self, base_url, url_suffix=""):
        self.base_url = base_url
        self.url_suffix = url_suffix
        self.url = base_url + url_suffix

        self.session = requests.Session()


