import allure


@allure.title("Создание питомца")
def test_create_pet(api_client):

    request_json = api_client.pet.generate_test_pet_data(type="valid")
    post_response = api_client.pet.post_pet(request_json)
    assert post_response.status_code == 200


@allure.title("Создание питомца с неверно заданным ID")
def test_try_create_pet_with_invalid_id(api_client):
        
    request_json = api_client.pet.generate_test_pet_data(type="invalid_id")
    post_response = api_client.pet.post_pet(request_json)
    assert post_response.status_code == 400
