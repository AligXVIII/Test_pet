import requests
from faker import Faker
import json
import allure
from pydantic import ValidationError
from pet_schema import Pet


PET_SERVICE_URL = "http://5.181.109.28:9090/api/v3"
METHOD = "PUT"
fake = Faker("ru_Ru")


@allure.title("Обновление данных питомца и проверка изменений")
def test_update_pet_information(create_and_delete_pet, log_response,log_request):

    with allure.step(
        "Получить ID питомца для обновления и подготовить новые данные питомца"
    ):
        METHOD = "PUT"
        ID_OF_THE_UPDATE_PET = create_and_delete_pet["id"]
        new_info_pet = {
            "id": ID_OF_THE_UPDATE_PET,
            "name": fake.first_name(),
            "status": fake.random_element(elements=("available", "sold", "pending")),
            "category": {"id": 1, "name": "dogs"},
            "tags": [{"id": 1, "name": "vip"}],
            "photoUrls": ["https://i.ytimg.com/vi/vPPx29Co0vk/maxresdefault.jpg"],
        }
        
        log_request(METHOD, f"{PET_SERVICE_URL}/pet", new_info_pet)

    with allure.step("Отправить запрос для обновления информации и проверить обновление питомца"):

        update_response = requests.put(f"{PET_SERVICE_URL}/pet", json=new_info_pet)

        log_response(update_response, METHOD, f"{PET_SERVICE_URL}/pet")

        assert update_response.status_code == 200

    with allure.step("Проверяем,что новый данные можно получить с помощью запроса get"):

        METHOD = "GET"

        get_response = requests.get(f"{PET_SERVICE_URL}/pet/{ID_OF_THE_UPDATE_PET}")

        log_response( get_response, METHOD, f"{PET_SERVICE_URL}/pet/{ID_OF_THE_UPDATE_PET}")

        assert get_response.status_code == 200

    with allure.step("Сравнить ответ с схемой Pet"):

        updated_data = get_response.json()
        
        try:
            validated_pet = Pet(**updated_data)
        except ValidationError as expect:
            assert False


@allure.title("Неверный путь для обновления данных")
def test_invalid_specified_path_for_update(create_and_delete_pet, log_response):

    with allure.step("Указать неверный путь"):
        update_response = requests.put( f"{PET_SERVICE_URL}/not_pet", json=create_and_delete_pet)

    with allure.step("Получить ошибку: Питомец не найден"):

        log_response(update_response, METHOD, f"{PET_SERVICE_URL}/not_pet")

        assert update_response.status_code == 404


@allure.title("Неккоректные данные для обновления")
def test_failed_update_due_to_an_invalid_pet_ID(log_response,log_request):

    with allure.step("Создаем питомца с неккоректным ID"):
        new_info_pet = {
            "id": "BC",
            "name": "Cat",
            "status": "sold",
        }
        
        log_request(METHOD, f"{PET_SERVICE_URL}/pet", new_info_pet)

    with allure.step("Получаем ошибку о неверных данных"):
        update_response = requests.put(f"{PET_SERVICE_URL}/pet", json=new_info_pet)

        log_response(update_response, METHOD, f"{PET_SERVICE_URL}/pet")

        assert update_response.status_code == 400


@allure.title("Недопустимая команда обновления данных")
def test_invalid_request_patch(create_and_delete_pet, log_response):

    with allure.step("Используем команду patch,недопустимый метод"):
        
        METHOD = "Patch"
        update_response = requests.patch(f"{PET_SERVICE_URL}/pet", json=create_and_delete_pet)

    with allure.step("Получаем статус код о недопустимом HTTP-методе"):
         
        log_response(update_response, METHOD, f"{PET_SERVICE_URL}/pet")

        assert update_response.status_code == 405
