import allure

@allure.title("Обновление данных питомца и проверка изменений")
def test_update_pet_information(create_and_delete_pet,app):

    new_info_pet = app.generate_factory.generate_test_pet_data(pet_id=create_and_delete_pet["id"], data_type="valid")
    update_response = app.api.pet.put_pet(new_info_pet)
    assert update_response.status_code == 200
    get_response = app.api.pet.get_pet(create_and_delete_pet["id"])
    assert get_response.status_code == 200
    assert app.api.pet.validate_pet_schema(get_response)

@allure.title("Обновление несуществующего питомца")
def test_invalid_specified_path_for_update(app):

    nonexistent_pet_data = app.generate_factory.generate_test_pet_data(pet_id=999999999,data_type="valid")
    update_response = app.api.pet.put_pet(nonexistent_pet_data)
    assert update_response.status_code == 404

@allure.title("Некоректные данные для обновления")
def test_failed_update_due_to_an_invalid_pet_ID(app):

    new_info_pet = app.generate_factory.generate_test_pet_data(data_type="invalid_id")
    update_response = app.api.pet.put_pet(new_info_pet) 
    assert update_response.status_code == 400

@allure.title("Недопустимая команда обновления данных")
def test_invalid_request_patch(create_and_delete_pet,app):

    update_response = app.api.pet.patch_pet(create_and_delete_pet['id'])       
    assert update_response.status_code == 405
