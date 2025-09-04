import requests
import json
import allure
from pydantic import ValidationError
from pet_schema import Pet 

PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.title("Обновление данных питомца и проверка изменений")   
def test_update_pet_information(create_and_delete_pet):

    with allure.step("Получить ID питомца для обновления и подготовить новые данные питомца"):
        ID_OF_THE_UPDATE_PET = create_and_delete_pet["id"]
        new_info_pet = {
            "id": ID_OF_THE_UPDATE_PET,
            "name": "Cat",
            "status": "sold",
            "category": {
                "id": 1,
                "name": "dogs"
            },
            "tags": [
                {
                    "id": 1,
                    "name": "vip"
                }
            ],
            "photoUrls": ["https://i.ytimg.com/vi/vPPx29Co0vk/maxresdefault.jpg"]
        }
        
        allure.attach(
            json.dumps(create_and_delete_pet, ensure_ascii=False, indent=2),
            "Изначальные данные",
            allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(new_info_pet, ensure_ascii=False, indent=2),
            "Обновленные данные",
            allure.attachment_type.JSON
        )
    
    with allure.step("Отправить запрос для обновления информации и проверить обновление питомца"):
        update_response = requests.put(f'{PET_SERVICE_URL}/pet', json=new_info_pet)
        assert update_response.status_code == 200

        allure.attach(
                f"Статус: {update_response.status_code}\n Данные: {update_response.text}",
            "Ответ сервера",
                allure.attachment_type.TEXT
            )
    

    with allure.step("Проверяем,что новый данные можно получить с помощью запроса get"):
        get_response = requests.get(f'{PET_SERVICE_URL}/pet/{ID_OF_THE_UPDATE_PET}')
        assert get_response.status_code == 200
        updated_data = get_response.json()
    
    with allure.step("Сравнить ответ с схемой Pet"):
        try:
            validated_pet = Pet(**updated_data)
        except ValidationError as expect:
            assert False

    with allure.step("Проверить корректность обновления всех полей"):
        assert validated_pet.name == new_info_pet["name"]
        assert validated_pet.status == new_info_pet["status"]
        assert validated_pet.category.id == new_info_pet["category"]["id"]
        assert validated_pet.category.name == new_info_pet["category"]["name"]
        assert len(validated_pet.tags) == len(new_info_pet["tags"])
        assert validated_pet.tags[0].id == new_info_pet["tags"][0]["id"]
        assert validated_pet.tags[0].name == new_info_pet["tags"][0]["name"]    

@allure.title('Неверный путь для обновления данных') 
def test_invalid_specified_path_for_update(create_and_delete_pet):
    
    with allure.step("Указать неверный путь"):
        update_response = requests.put(f'{PET_SERVICE_URL}/not_pet', json=create_and_delete_pet)    
    
    with allure.step("Получить ошибку: Питомец не найден"):
        assert update_response.status_code == 404
    
        allure.attach(
                f"Статус: {update_response.status_code}",
               "Ответ сервера",
                allure.attachment_type.TEXT
            )


@allure.title('Неккоректные данные для обновления') 
def test_failed_update_due_to_an_invalid_pet_ID():

    with allure.step("Создаем питомца с неккоректным ID"):
        new_info_pet = {
        "id": 'BC',
        "name": "Cat",
        "status": "sold",
    }
    
        allure.attach(
            json.dumps(new_info_pet, ensure_ascii=False, indent=2),
            "Данные с неккоректным ID",
            allure.attachment_type.JSON
        )

    with allure.step("Получаем ошибку о неверных данных"):
        update_response = requests.put(f'{PET_SERVICE_URL}/pet', json=new_info_pet)    
        assert update_response.status_code == 400

        allure.attach(
             f"Статус: {update_response.status_code}",
            "Ответ сервера",
             allure.attachment_type.TEXT
        )

@allure.title('Недопустимая команда обновления данных') 
def test_invalid_request_patch(create_and_delete_pet):
    with allure.step("Используем команду patch,недопустимый метод"):
        update_response = requests.patch(f'{PET_SERVICE_URL}/pet', json=create_and_delete_pet) 

    with allure.step("Получаем статус код о недопустимом HTTP-методе"):
        assert update_response.status_code == 405
        allure.attach(
             f"Статус: {update_response.status_code}",
            "Ответ сервера",
             allure.attachment_type.TEXT
        )