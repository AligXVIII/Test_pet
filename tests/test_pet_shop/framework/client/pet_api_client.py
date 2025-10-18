from tests.test_pet_shop.constants import PET_SERVICE_URL
from tests.test_pet_shop.framework.client.base_api_client import BaseAPIClient
from pydantic import ValidationError
from schemes.pet_schema import Pet
from utils import log_response,log_request
from faker import Faker
import random
import allure


class PetAPIClient(BaseAPIClient):

    def __init__(self):
        super().__init__(base_url=PET_SERVICE_URL, url_suffix="/pet")


    @allure.step("Запрос на создание питомца")
    def post_pet(self, pet_data):
        log_request("POST", f"{PET_SERVICE_URL}/pet", pet_data)
        response = self.session.post(self.url, json=pet_data)
        log_response(response)
        return response
    
    @allure.step("Запрос на удаление питомца")
    def delete_pet(self, pet_id):
        log_request("DELETE", f"{PET_SERVICE_URL}/pet", None)
        response = self.session.delete(url=f"{self.url}/{pet_id}")
        log_response(response)
        return response

    @allure.step("Запрос на получение питомца")
    def get_pet(self, pet_id):
        url = f"{self.url}/{pet_id}"
        log_request("GET", url, None)
        response = self.session.get(url=f"{self.url}/{pet_id}")
        log_response(response)
        return response
    

    @allure.step("Запрос на обновление питомца")
    def put_pet(self, pet_data):
        log_request("PUT", f"{PET_SERVICE_URL}/pet", pet_data)
        response = self.session.put(self.url, json=pet_data)
        log_response(response)
        return response
    
    
    @allure.step("Недопустимый запрос patch питомца")
    def patch_pet(self, pet_id):
        url = f"{self.url}/{pet_id}"
        log_request("PATCH", url, None)
        response = self.session.patch(url)
        log_response(response)
        return response
     
    def log_search_criteria(self, search_value, criteria_type):
        step_descriptions = {
            "id": "Задаем ID питомца,информацию о котором мы хотим узнать",
            "name": "Задаем имя,по которому будем искать информацию", 
            "nonexistent_id": "Задаем ID,которого нет в базе"
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


    @allure.step("Генерация случайного питомца")
    def generate_test_pet_data(self,pet_id = None,type="valid"):
        fake = Faker("ru_Ru")

        if pet_id == None:
            pet_id = random.randint(1, 1000)
    
        pet = {
            "valid": {
                "id": pet_id,
                "name": fake.first_name(),
                "status": fake.random_element(elements=("available", "sold", "pending")),
                "category": {"id": 1, "name": "dogs"},
                "tags": [{"id": 1, "name": "vip"}],
                "photoUrls": ["https://i.ytimg.com/vi/vPPx29Co0vk/maxresdefault.jpg"]
            },

            "invalid_id": {
                "id": "abxc",
                "name": fake.first_name(),
                "status": fake.random_element(elements=("available", "sold"))
            },
            "empty_name": {
                "id": pet_id,
                "name": "",
                "status": "available"
            }
        }
    
        return pet[type]
    


    @allure.step("Валидация ответа по схеме Pet")
    def validate_pet_schema(self, response):
        response_data = response.json()
        try:
            validated_pet = Pet(**response_data)
            allure.attach(
                "Валидация прошла успешно",
                "Проверка схемы Pet",
                allure.attachment_type.TEXT
            )
            return True
        except ValidationError as e:
            allure.attach(
                f"Ошибка валидации: {str(e)}",
                "Ошибка схемы Pet",
                allure.attachment_type.TEXT
            )
            return False
    


    def upload_image_for_pet(self, pet_id, file):
        response = self.session.post(url=f"{self.url}/{pet_id}/uploadImage", files=file)
        log_response(response)
        return response