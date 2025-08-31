import requests
import json
import allure

PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.title("Удаление питомца по ID")       
def test_deleted_pet(create_pet):

    with allure.step("Отправляем запрос на удаление по ID питомца"): 
        DELETE_PET_ID = create_pet['id']
        response = requests.delete(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
        allure.attach(
            f"Статус: {response.status_code}",
            "Ответ сервера на запрос delete",
            allure.attachment_type.TEXT
        )
        assert response.status_code == 200
    
    with allure.step("Проверяем,что питомца больше нельзя найти"): 
        requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
        allure.attach(
            f"Статус: {requests_response.status_code}",
            "Ответ сервера на запрос get после удаления",
            allure.attachment_type.TEXT
        )
        assert requests_response.status_code == 404



@allure.title("Удаление питомца по имени")   
def test_try_delete_pet_by_name(create_pet):

    with allure.step("Отправляем запрос на удаление по имени питомца и получаем ошибку"): 
        PET_NAME = create_pet['name']
        TRUE_PET_ID = create_pet['id']

        response = requests.delete(f'{PET_SERVICE_URL}/pet/{PET_NAME}')
        allure.attach(
            f"Статус: {response.status_code}",
            "Ответ сервера на запрос get после удаления",
            allure.attachment_type.TEXT
        )
        assert response.status_code == 400
    
    with allure.step("Отправляем запрос get,чтобы проверить,что питомец остался в базе"): 
        requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{TRUE_PET_ID}')
        allure.attach(
            f"Статус: {requests_response.status_code}",
            "Ответ сервера на запрос get после удаления",
            allure.attachment_type.TEXT
        )
        assert requests_response.status_code == 200
