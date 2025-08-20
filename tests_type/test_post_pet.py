import pytest
import requests
from faker  import Faker
import random
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'


def test_create_pet():
    
    fake = Faker('ru_Ru')

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)
    assert response.status_code == 200

def test_invalid_input_pet():
    
    request_json = {
      "id": 'abxc',
      "name":"Dog",
      "status": "available"
    }
    response = requests.post(f'{PET_SERVICE_URL}/pet', json=request_json)

    assert response.status_code == 400