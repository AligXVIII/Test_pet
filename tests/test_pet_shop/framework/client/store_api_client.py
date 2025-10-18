from tests.test_pet_shop.constants import PET_SERVICE_URL
from tests.test_pet_shop.framework.client.base_api_client import BaseAPIClient


class StoreAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/store")


    def create_store(self):
        return 'creating store'

