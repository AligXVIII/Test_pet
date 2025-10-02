import pytest
import json
import allure
import requests
from faker  import Faker
import random
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'

             
@pytest.fixture(scope='module')
def create_and_delete_pet():
    METHOD = 'POST'
    fake = Faker('ru_Ru')

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold',"pending"))
    }
    response = requests.post(PET_SERVICE_URL+'/pet', json=request_json)

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
    yield response.json()
    response = requests.delete(PET_SERVICE_URL+f'/pet/{request_json["id"]}')


@pytest.fixture(scope='function')
def create_pet():
    fake = Faker('ru_Ru')
    METHOD = 'POST'

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }
    response = requests.post(PET_SERVICE_URL+'/pet', json=request_json)

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
    return response.json()
