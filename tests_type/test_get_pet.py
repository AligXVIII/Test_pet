import requests

PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'

def test_successful_get_pet_id(create_and_delete_pet):
    pet_id = create_and_delete_pet['id']
    
    response = requests.get(f'{PET_SERVICE_URL}/pet/{pet_id}')
    response_json = response.json()

    assert response.status_code == 200
    assert create_and_delete_pet['name'] == response_json['name']

def test_get_by_name_and_check_failed(create_and_delete_pet):
 
    pet_name = create_and_delete_pet['name']
    response = requests.get(f'{PET_SERVICE_URL}/pet/{pet_name}')

    assert response.status_code == 400

def test_get_pet_by_nonexistent_id():

    nonexistent_id = 999999999
    response = requests.get(f'{PET_SERVICE_URL}/pet/{nonexistent_id}')

    assert response.status_code == 404