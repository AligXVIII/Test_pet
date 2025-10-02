import pytest
import json
import allure
import requests
from faker  import Faker
import random
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'
METHOD = 'POST'

@allure.title("Создание питомца")   
def test_create_pet():
  with allure.step("Задаем данные для создания питомца"):
    
    fake = Faker('ru_Ru')
    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }
    
    req = requests.Request('POST', f'{PET_SERVICE_URL}/pet', json=request_json)
    prepared = req.prepare()
    headers = [f"{k}:{v}" for k, v in prepared.headers.items()]

    basic_data = {
        "Метод запроса": METHOD,
        "Адрес": PET_SERVICE_URL+'/pet',
        "Заголовок запроса": headers,
        "Тело запроса": request_json,
        }
    
    allure.attach(
      json.dumps(basic_data, ensure_ascii=False, indent=2),
      "Request log",
      allure.attachment_type.JSON
    )
  
  with allure.step("Проверяем успешность обработки запроса"):
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)
    
    headers_responce = [f"{k}: {v}" for k, v in response.headers.items()]
    request_body = json.loads(response.text)

    put_responce_server = {
      "Метод запроса": METHOD,
      "Адрес": PET_SERVICE_URL+'/pet',
      "Заголовок ответа": headers_responce,
      "Тело ответа": request_body,
      "Статус": response.status_code
        }
        
    allure.attach(
      json.dumps(put_responce_server, ensure_ascii=False, indent=2),
      "Request log",
      allure.attachment_type.JSON
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
    
    req = requests.Request('POST', f'{PET_SERVICE_URL}/pet', json=request_json)
    prepared = req.prepare()
    headers = [f"{k}:{v}" for k, v in prepared.headers.items()]

    basic_data = {
        "Метод запроса": METHOD,
        "Адрес": PET_SERVICE_URL+'/pet',
        "Заголовок запроса": headers,
        "Тело запроса": request_json,
        }
    
    allure.attach(
      json.dumps(basic_data, ensure_ascii=False, indent=2),
      "Request log",
      allure.attachment_type.JSON
    )
    
  with allure.step("Получаем ошибку о некорректных параметрах запроса"):
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)
     
    headers_responce = [f"{k}: {v}" for k, v in response.headers.items()]
    request_body = json.loads(response.text)
    put_responce_server = {
      "Метод запроса": METHOD,
      "Адрес": PET_SERVICE_URL+'/pet',
      "Заголовок ответа": headers_responce,
      "Тело ответа": request_body,
      "Статус": response.status_code
        }
        
    allure.attach(
      json.dumps(put_responce_server, ensure_ascii=False, indent=2),
      "Request log",
      allure.attachment_type.JSON
      )
    
    assert response.status_code == 400