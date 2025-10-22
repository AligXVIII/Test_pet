from constants import PET_SERVICE_URL
from framework.client.base_api_client import BaseAPIClient
from utils import log_response,log_request
import allure


class StoreAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/store")

    @allure.step("Запрос на получение инвентаря")
    def get_inventory(self):
        url = f"{self.url}/inventory"
        log_request("GET", url, None)
        response = self.session.get(url)
        log_response(response)
        return response
    
    @allure.step("Запрос на оформление нового заказа в магазине")
    def post_order(self,order_data):
        url = f"{self.url}/order"
        log_request("POST", url,order_data)
        response = self.session.post(url, json = order_data)
        log_response(response)
        return response

    @allure.step("Запрос на получение заказа по индефикатору")
    def get_order(self, orderID):
        url = f"{self.url}/order/{orderID}"
        log_request("GET", url, None)
        response = self.session.get(url)
        log_response(response)
        return response
    
    @allure.step("Запрос на удаление заказа")
    def delete_order(self,orderID):
        url = f"{self.url}/order/{orderID}"
        log_request("DELETE", url, None)
        response = self.session.delete(url)
        log_response(response)
        return response


  