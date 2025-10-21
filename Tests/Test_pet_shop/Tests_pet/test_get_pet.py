import requests
import json
import allure
from utils import log_response, log_request 
PET_SERVICE_URL = "http://5.181.109.28:9090/api/v3"

@allure.title("Получение информации о питомце по ID")
def test_successful_get_pet_id(create_and_delete_pet):
    with allure.step("Задаем ID питомца,информацию о котором мы хотим узнать"):

        pet_id = create_and_delete_pet["id"]
        allure.attach(f"ID: {pet_id}", "ID питомца", allure.attachment_type.TEXT)


    with allure.step("Отправляем запрос get и проверяем успешность запроса"):

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{pet_id}")
        log_response(get_response)
        assert get_response.status_code == 200


    with allure.step("Проверяем,что имя питомца,которого мы создали совпадает с полученной информацией от запроса"):

        get_response_json = get_response.json()
        assert create_and_delete_pet["name"] == get_response_json["name"]


@allure.title("Неудачное получение информации о питомце по имени")
def test_get_by_name_and_check_failed(create_and_delete_pet):

    with allure.step("Задаем имя,по которому будем искать информацию"):

        pet_name = create_and_delete_pet["name"]
        allure.attach(f"Имя: {pet_name}", "Имя питомца", allure.attachment_type.TEXT)


    with allure.step("Получаем ошибку, что сервер не смог обработать запрос"):

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{pet_name}")
        log_response(get_response)
        assert get_response.status_code == 400


@allure.title("Неудачное получение информации о питомце с несуществующим ID")
def test_get_pet_by_nonexistent_id():

    with allure.step("Задаем ID,которого нет в базе"):

        nonexistent_id = 999999999
        allure.attach(f"{nonexistent_id}", "Заданный ID", allure.attachment_type.TEXT)


    with allure.step("Отправляем запрос на несуществующий ID и получаем ошибку:Питомец не найден"):

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{nonexistent_id}")
        log_response(get_response)
        assert get_response.status_code == 404
