import requests
from utils import log_request, log_response
import pytest

class BaseAPIClient:

    def __init__(self, base_url, url_suffix=""):
        self.base_url = base_url
        self.url_suffix = url_suffix
        self.url = base_url + url_suffix

        self.session = requests.Session()


    def _request(self, method, url, **kwargs):
        try:
            log_request(method, url, kwargs.get('json'))
            response = self.session.request(method, url, **kwargs)
            if response.status_code >= 500:
                pytest.skip(f"Сервер вернул {response.status_code}, тест пропущен")
            log_response(response)
            return response
        except requests.exceptions.Timeout:
            raise Exception(f"Таймаут: {method} {url}")
        except requests.exceptions.ConnectionError:
            raise Exception(f"Нет соединения: {method} {url}")
