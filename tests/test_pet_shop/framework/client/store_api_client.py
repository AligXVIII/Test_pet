from constants import PET_SERVICE_URL
from framework.client.base_api_client import BaseAPIClient
import allure


class StoreAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/store")

    @allure.step("Запрос на получение инвентаря")
    def get_inventory(self):
        return self._request("GET", f"{self.url}/inventory")

    @allure.step("Запрос на оформление нового заказа в магазине")
    def post_order(self, order_data):
        return self._request("POST", f"{self.url}/order", json=order_data)

    @allure.step("Запрос на получение заказа по идентификатору")
    def get_order(self, order_id):
        return self._request("GET", f"{self.url}/order/{order_id}")

    @allure.step("Запрос на удаление заказа")
    def delete_order(self, order_id):
        return self._request("DELETE", f"{self.url}/order/{order_id}")