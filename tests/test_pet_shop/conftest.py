import pytest
from tests.test_pet_shop.framework.entry_point.application import Application


@pytest.fixture
def api_client():
    return Application().api 

@pytest.fixture(scope="function")
def create_pet(api_client):

    request_json = api_client.pet.generate_test_pet_data()
    response = api_client.pet.post_pet(request_json)
    return response.json()

@pytest.fixture(scope="function")
def create_and_delete_pet(api_client, create_pet):
    
    pet_data = create_pet
    yield pet_data  
    api_client.pet.delete_pet(pet_data["id"])