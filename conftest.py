import pytest
import requests
from faker  import Faker
import random
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'

             
@pytest.fixture(scope='module')
def create_and_delete_pet():
    fake = Faker('ru_Ru')

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }
    response = requests.post(PET_SERVICE_URL+'/pet', json=request_json)
    
    yield response.json()
    response = requests.delete(PET_SERVICE_URL+f'/pet/{request_json["id"]}')


@pytest.fixture(scope='function')
def create_pet():
    fake = Faker('ru_Ru')

    request_json = {
      "id": random.randint(1,1000),
      "name": fake.first_name(),
      "status": fake.random_element(elements=('available','sold'))
    }
    response = requests.post(PET_SERVICE_URL+'/pet', json=request_json)
    
    return response.json()
