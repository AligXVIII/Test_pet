import pytest
import json
import allure
import requests
from faker import Faker
import random
from utils import log_response, log_request 
PET_SERVICE_URL = "http://5.181.109.28:9090/api/v3"


@allure.title("Создание питомца")
def test_create_pet():
    with allure.step("Задаем данные для создания питомца"):

        fake = Faker("ru_Ru")
        request_json = {
            "id": random.randint(1, 1000),
            "name": fake.first_name(),
            "status": fake.random_element(elements=("available", "sold")),
        }
    
        log_request("POST", f"{PET_SERVICE_URL}/pet", request_json)


    with allure.step("Проверяем успешность обработки запроса"):

        post_response = requests.post(f"{PET_SERVICE_URL}/pet", json=request_json)
        log_response(post_response)
        assert post_response.status_code == 200


@allure.title("Создание питомца с неверно заданным ID")
def test_try_create_pet_with_invalid_id():
    with allure.step("Задаем данные питомца с неверный типом ID"):
        
        request_json = {
            "id": "abxc",
            "name": "Dog", 
            "status": "available"
          }
 
        log_request("POST", f"{PET_SERVICE_URL}/pet", request_json)


    with allure.step("Получаем ошибку о некорректных параметрах запроса"):

        post_response = requests.post(f"{PET_SERVICE_URL}/pet", json=request_json)
        log_response(post_response)
        assert post_response.status_code == 400
