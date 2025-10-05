import pytest
import json
import allure
import requests
from faker import Faker
import random
from utils import log_request 

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
    log_request("POST", f"{PET_SERVICE_URL}/pet", request_json)
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
    log_request("POST", f"{PET_SERVICE_URL}/pet", request_json)
    return response.json()