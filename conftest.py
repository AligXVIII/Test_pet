import pytest
import json
import allure
import requests
from faker import Faker
import random

PET_SERVICE_URL = "http://5.181.109.28:9090/api/v3"


@pytest.fixture(scope="module")
def create_and_delete_pet():
    METHOD = "POST"
    fake = Faker("ru_Ru")

    request_json = {
        "id": random.randint(1, 1000),
        "name": fake.first_name(),
        "status": fake.random_element(elements=("available", "sold", "pending")),
    }
    response = requests.post(PET_SERVICE_URL + "/pet", json=request_json)

    req = requests.Request("POST", f"{PET_SERVICE_URL}/pet", json=request_json)
    prepared = req.prepare()
    headers = [f"{k}:{v}" for k, v in prepared.headers.items()]

    basic_data = {
        "Метод запроса": METHOD,
        "Адрес": PET_SERVICE_URL + "/pet",
        "Заголовок запроса": headers,
        "Тело запроса": request_json,
    }

    allure.attach(
        json.dumps(basic_data, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON,
    )
    yield response.json()
    response = requests.delete(PET_SERVICE_URL + f'/pet/{request_json["id"]}')


@pytest.fixture(scope="function")
def create_pet():
    fake = Faker("ru_Ru")
    METHOD = "POST"

    request_json = {
        "id": random.randint(1, 1000),
        "name": fake.first_name(),
        "status": fake.random_element(elements=("available", "sold")),
    }
    response = requests.post(PET_SERVICE_URL + "/pet", json=request_json)

    req = requests.Request("POST", f"{PET_SERVICE_URL}/pet", json=request_json)
    prepared = req.prepare()
    headers = [f"{k}:{v}" for k, v in prepared.headers.items()]

    basic_data = {
        "Метод запроса": METHOD,
        "Адрес": PET_SERVICE_URL + "/pet",
        "Заголовок запроса": headers,
        "Тело запроса": request_json,
    }

    allure.attach(
        json.dumps(basic_data, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON,
    )
    return response.json()


@pytest.fixture(scope="function")
def log_response():
    def _log_form(response, method, url):
        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]

        try:
            if response.text.strip():
                response_body = json.loads(response.text)
            else:
                response_body = "(пустой ответ)"
        except (json.JSONDecodeError, AttributeError):
            response_body = response.text

        log_data = {
            "Метод запроса": method,
            "Адрес": url,
            "Заголовок ответа": headers_response,
            "Тело ответа": response_body,
            "Статус": response.status_code,
        }

        allure.attach(
            json.dumps(log_data, ensure_ascii=False, indent=2),
            "Response log",
            allure.attachment_type.JSON,
        )
        return response

    return _log_form



@pytest.fixture(scope='function')
def log_request():   
    def _log_request(method, url, request_body):

        req = requests.Request(method, url, json=request_body)
        prepared = req.prepare()
        headers = [f"{k}: {v}" for k, v in prepared.headers.items()]

        request_data = {
            "Метод запроса": method,
            "Адрес": url,
            "Заголовок запроса": headers,
            "Тело запроса": request_body,
        }


        allure.attach(
            json.dumps(request_data, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        
        return request_data
    
    return _log_request