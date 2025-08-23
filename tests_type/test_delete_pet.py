import requests

PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'
    
def test_deleted_pet(create_pet):

    DELETE_PET_ID = create_pet['id']

    response = requests.delete(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
    assert response.status_code == 200

    requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
    assert requests_response.status_code == 404


def test_try_delete_pet_by_name(create_pet):

    PET_NAME = create_pet['name']
    TRUE_PET_ID = create_pet['id']

    
    response = requests.delete(f'{PET_SERVICE_URL}/pet/{PET_NAME}')
    assert response.status_code == 400

    requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{TRUE_PET_ID}')
    assert requests_response.status_code == 200
