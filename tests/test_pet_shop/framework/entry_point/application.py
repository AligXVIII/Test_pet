from framework.factories.api_factory import APIFactory
from framework.factories.generate_factory import GenerateFactory

class Application:

    def __init__(self):
        self._api = None
        self._data_factory = None

    @property
    def api(self):
        if self._api is None:
            self._api = APIFactory()
        return self._api

    @property
    def generate_factory(self):
        if self._data_factory is None:
            self._data_factory = GenerateFactory()
        return self._data_factory

