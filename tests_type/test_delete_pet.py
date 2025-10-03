import requests
import json
import allure

PET_SERVICE_URL = "http://5.181.109.28:9090/api/v3"


@allure.title("Удаление питомца по ID")
def test_deleted_pet(create_pet, log_response):

    with allure.step("Отправляем запрос на удаление по ID питомца"):
        METHOD = "DELETE"
        DELETE_PET_ID = create_pet["id"]

        delete_response = requests.delete(f"{PET_SERVICE_URL}/pet/{DELETE_PET_ID}")

        log_response(delete_response, METHOD, f"{PET_SERVICE_URL}/pet/{DELETE_PET_ID}")

        assert delete_response.status_code == 200

    with allure.step("Проверяем,что питомца больше нельзя найти"):
        METHOD = "GET"

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{DELETE_PET_ID}")

        log_response(get_response, METHOD, f"{PET_SERVICE_URL}/pet/{DELETE_PET_ID}")

        assert get_response.status_code == 404


@allure.title("Удаление питомца по имени")
def test_try_delete_pet_by_name(create_pet, log_response):

    with allure.step(
        "Отправляем запрос на удаление по имени питомца и получаем ошибку"
    ):
        METHOD = "DELETE"
        PET_NAME = create_pet["name"]
        TRUE_PET_ID = create_pet["id"]

        delete_response = requests.delete(f"{PET_SERVICE_URL}/pet/{PET_NAME}")

        log_response(delete_response, METHOD, f"{PET_SERVICE_URL}/pet/{PET_NAME}")

        assert delete_response.status_code == 400

    with allure.step(
        "Отправляем запрос get,чтобы проверить,что питомец остался в базе"
    ):
        METHOD = "GET"

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{TRUE_PET_ID}")

        log_response(get_response, METHOD, f"{PET_SERVICE_URL}/pet/{TRUE_PET_ID}")

        assert get_response.status_code == 200
