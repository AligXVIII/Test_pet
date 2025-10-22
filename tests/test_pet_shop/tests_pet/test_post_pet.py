import allure


@allure.title("Создание питомца")
def test_create_pet(app):

    request_json = app.generate_factory.generate_test_pet_data(data_type="valid")
    post_response = app.api.pet.post_pet(request_json)
    assert post_response.status_code == 200


@allure.title("Создание питомца с неверно заданным ID")
def test_try_create_pet_with_invalid_id(app):
        
    request_json = app.generate_factory.generate_test_pet_data(data_type="invalid_id")
    post_response = app.api.pet.post_pet(request_json)
    assert post_response.status_code == 400
