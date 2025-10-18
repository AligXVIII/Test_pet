import allure



@allure.title("Обновление данных питомца и проверка изменений")
def test_update_pet_information(create_and_delete_pet,api_client):

    new_info_pet = api_client.pet.generate_test_pet_data(pet_id=create_and_delete_pet["id"], type="valid")

    update_response = api_client.pet.put_pet(new_info_pet)
    assert update_response.status_code == 200

    get_response = api_client.pet.get_pet(create_and_delete_pet["id"])
    assert get_response.status_code == 200

    assert api_client.pet.validate_pet_schema(get_response)



@allure.title(" обновление несуществующего питомца")
def test_invalid_specified_path_for_update(api_client):

    nonexistent_pet_data = api_client.pet.generate_test_pet_data(pet_id=999999999,type="valid")
    update_response = api_client.pet.put_pet(nonexistent_pet_data)
    assert update_response.status_code == 404

@allure.title("Неккоректные данные для обновления")
def test_failed_update_due_to_an_invalid_pet_ID(api_client):

    new_info_pet = api_client.pet.generate_test_pet_data(type="invalid_id")
    update_response = api_client.pet.put_pet(new_info_pet) 
    assert update_response.status_code == 400

@allure.title("Недопустимая команда обновления данных")
def test_invalid_request_patch(create_and_delete_pet,api_client):

    update_response = api_client.pet.patch_pet(create_and_delete_pet['id'])       
    assert update_response.status_code == 405
