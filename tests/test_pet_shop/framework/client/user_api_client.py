from constants import PET_SERVICE_URL
from framework.client.base_api_client import BaseAPIClient
import allure


class UserAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/user")

    @allure.step("Запрос на создание пользователя")
    def post_user(self, user_data):
        return self._request("POST", self.url, json=user_data)

    @allure.step("Создание списка пользователей")
    def post_users_list(self, users_data):
        return self._request("POST", f"{self.url}/createWithList", json=users_data)

    @allure.step("Логин пользователя в систему")
    def get_user_login(self, username, password):
        params = {"username": username, "password": password}
        return self._request("GET", f"{self.url}/login", params=params)

    @allure.step("Вывод пользователя из системы")
    def get_user_logout(self):
        return self._request("GET", f"{self.url}/logout")

    @allure.step("Получение пользователя по username")
    def get_user_by_username(self, username):
        return self._request("GET", f"{self.url}/{username}")

    @allure.step("Обновление пользователя")
    def put_user(self, username, user_data):
        return self._request("PUT", f"{self.url}/{username}", json=user_data)

    @allure.step("Удаление пользователя")
    def delete_user(self, username):
        return self._request("DELETE", f"{self.url}/{username}")