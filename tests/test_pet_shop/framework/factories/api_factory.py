from tests.test_pet_shop.framework.client.pet_api_client import PetAPIClient
from tests.test_pet_shop.framework.client.store_api_client import StoreAPIClient


class APIFactory:

    def __init__(self):
        self._pet = None
        self._store = None

    @property
    def pet(self):
        if self._pet is None:
            self._pet = PetAPIClient()
        return self._pet

    @property
    def store(self):
        if self._store is None:
            self._store = StoreAPIClient()
        return self._store
