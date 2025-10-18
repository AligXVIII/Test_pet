import allure

@allure.title("Удаление питомца по ID")
def test_deleted_pet(create_pet,api_client):
    
    delete_response = api_client.pet.delete_pet(create_pet["id"])
    assert delete_response.status_code == 200

    get_response = api_client.pet.get_pet(create_pet["id"])
    assert get_response.status_code == 404

@allure.title("Удаление питомца по имени")
def test_try_delete_pet_by_name(create_pet,api_client):

    delete_response = api_client.pet.delete_pet(create_pet["name"])
    assert delete_response.status_code == 400

    get_response = api_client.pet.get_pet(create_pet["id"])
    assert get_response.status_code == 200
