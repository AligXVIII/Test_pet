from constants import PET_SERVICE_URL
from framework.client.base_api_client import BaseAPIClient
from utils import log_response,log_request
import allure


class UserAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/user")

    @allure.step("Запрос на создание пользователя")
    def post_user(self,user_data):
        log_request("POST", self.url,user_data)
        response = self.session.post(self.url, json = user_data)
        log_response(response)
        return response
    

    @allure.step("Создание списка пользователей")
    def post_users_list(self, users_data):
        url = f"{self.url}/createWithList"
        log_request("POST", url, users_data)
        response = self.session.post(url, json=users_data)
        log_response(response)
        return response

    @allure.step("Логин пользователя в систему")
    def get_user_login(self, username, password):
        url = f"{self.url}/login"
        params = {"username": username, "password": password}
        log_request("GET", url, params)
        response = self.session.get(url, params=params)
        log_response(response)
        return response


    @allure.step("Вывод пользователя из системы")
    def get_user_logout(self):
        url = f"{self.url}/logout"
        log_request("GET", url, None)
        response = self.session.get(url)
        log_response(response)
        return response


    @allure.step("Получение пользователя по username")
    def get_user_by_username(self, username):
        url = f"{self.url}/{username}"
        log_request("GET", url, None)
        response = self.session.get(url)
        log_response(response)
        return response

    @allure.step("Обновление пользователя")
    def put_user(self, username, user_data):
        url = f"{self.url}/{username}"
        log_request("PUT", url, user_data)
        response = self.session.put(url, json=user_data)
        log_response(response)
        return response

    @allure.step("Удаление пользователя")
    def delete_user(self, username):
        url = f"{self.url}/{username}"
        log_request("DELETE", url, None)
        response = self.session.delete(url)
        log_response(response)
        return response
