import allure
from constants import  nonexistent_id 

@allure.title("Получение информации о питомце по ID")
def test_successful_get_pet_id(create_and_delete_pet,api_client):
  
    api_client.pet.log_search_criteria(create_and_delete_pet["id"], "id")
    get_response = api_client.pet.get_pet(create_and_delete_pet["id"])
    assert get_response.status_code == 200
    api_client.pet.validate_pet_data(get_response, create_and_delete_pet)


@allure.title("Неудачное получение информации о питомце по имени")
def test_get_by_name_and_check_failed(create_and_delete_pet,api_client):

    api_client.pet.log_search_criteria(create_and_delete_pet["name"], "name")
    get_response = api_client.pet.get_pet(create_and_delete_pet["name"])
    assert get_response.status_code == 400


@allure.title("Неудачное получение информации о питомце с несуществующим ID")
def test_get_pet_by_nonexistent_id(api_client):
   
    api_client.pet.log_search_criteria(nonexistent_id, "nonexistent_id")
    get_response = api_client.pet.get_pet(nonexistent_id)
    assert get_response.status_code == 404
