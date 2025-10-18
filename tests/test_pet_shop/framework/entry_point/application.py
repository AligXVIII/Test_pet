from tests.test_pet_shop.framework.factories.api_factory import APIFactory


class Application:

    def __init__(self):
        self._api = None

    @property
    def api(self):
        if self._api is None:
            self._api = APIFactory()
        return self._api




