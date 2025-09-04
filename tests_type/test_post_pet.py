import pytest
import json
import allure
import requests
from faker  import Faker
import random
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.title("Создание питомца")   
def test_create_pet():
  with allure.step("Задаем данные для создания питомца"):
    fake = Faker('ru_Ru')

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }

    allure.attach(
      json.dumps(request_json, ensure_ascii=False, indent=2),
      "Данные нового питомца",
      allure.attachment_type.JSON
        )
  
  with allure.step("Проверяем успешность обработки запроса"):
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)
    allure.attach(
      f"Статус: {response.status_code}",
      "Ответ сервера",
      allure.attachment_type.TEXT
    )
    assert response.status_code == 200


@allure.title("Создание питомца с неверно заданным ID")   
def test_try_create_pet_with_invalid_id():
  with allure.step("Задаем данные питомца с неверный типом ID"):
    request_json = {
        "id": 'abxc',
        "name":"Dog",
        "status": "available"
    }
    allure.attach(
      json.dumps(request_json, ensure_ascii=False, indent=2),
      "Данные питомца с неправильным ID",
      allure.attachment_type.JSON
        )
    
  with allure.step("Получаем ошибку о некорректных параметрах запроса"):
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)
    allure.attach(
      f"Статус: {response.status_code}",
      "Ответ сервера",
      allure.attachment_type.TEXT
      )
    assert response.status_code == 400