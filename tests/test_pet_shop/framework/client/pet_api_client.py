from constants import PET_SERVICE_URL
from framework.client.base_api_client import BaseAPIClient
from schemes.pet_schema import Pet
from pydantic import ValidationError
import allure
import json


class PetAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/pet")

    @allure.step("Запрос на создание питомца")
    def post_pet(self, pet_data):
        return self._request("POST", self.url, json=pet_data)

    @allure.step("Запрос на удаление питомца")
    def delete_pet(self, pet_id):
        return self._request("DELETE", f"{self.url}/{pet_id}")

    @allure.step("Запрос на получение питомца")
    def get_pet(self, pet_id):
        return self._request("GET", f"{self.url}/{pet_id}")

    @allure.step("Запрос на обновление питомца")
    def put_pet(self, pet_data):
        return self._request("PUT", self.url, json=pet_data)

    @allure.step("Недопустимый запрос patch питомца")
    def patch_pet(self, pet_id):
        return self._request("PATCH", f"{self.url}/{pet_id}")

    def log_search_criteria(self, search_value, criteria_type):
        step_descriptions = {
            "id": "Задаем ID питомца, информацию о котором мы хотим узнать",
            "name": "Задаем имя, по которому будем искать информацию",
            "nonexistent_id": "Задаем ID, которого нет в базе"
        }
        attachment_descriptions = {
            "id": "Поиск по корректному ID",
            "name": "Попытка поиска по имени (некорректно)",
            "nonexistent_id": "Поиск по несуществующему ID"
        }
        with allure.step(step_descriptions[criteria_type]):
            allure.attach(str(search_value), attachment_descriptions[criteria_type], allure.attachment_type.TEXT)

    @allure.step("Проверка данных питомца")
    def validate_pet_data(self, actual_response, expected_data, fields_to_check=None):
        if fields_to_check is None:
            fields_to_check = ["id", "name", "status"]
        response_json = actual_response.json()
        for field in fields_to_check:
            expected_value = expected_data[field]
            actual_value = response_json[field]
            assert actual_value == expected_value, f"Поле {field}: ожидалось {expected_value}, получено {actual_value}"
            allure.attach(
                f"Поле: {field}\nОжидалось: {expected_value}\nПолучено: {actual_value}",
                f"Проверка поля {field}",
                allure.attachment_type.TEXT
            )

    @allure.step("Валидация ответа по схеме Pet")
    def validate_pet_schema(self, response):
        try:
            response_data = response.json()
            Pet(**response_data)
            allure.attach("Валидация прошла успешно", "Проверка схемы Pet", allure.attachment_type.TEXT)
            return True
        except (ValidationError, json.JSONDecodeError) as e:
            allure.attach(f"Ошибка валидации: {str(e)}", "Ошибка схемы Pet", allure.attachment_type.TEXT)
            return False

    def upload_image_for_pet(self, pet_id, file):
        return self._request("POST", f"{self.url}/{pet_id}/uploadImage", files=file)