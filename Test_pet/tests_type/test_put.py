import requests
from faker  import Faker
import json
import allure
from pydantic import ValidationError
from pet_schema import Pet 


PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'
METHOD = 'PUT'
fake = Faker('ru_Ru')

@allure.title("Обновление данных питомца и проверка изменений")   
def test_update_pet_information(create_and_delete_pet):

    METHOD = 'PUT'
    with allure.step("Получить ID питомца для обновления и подготовить новые данные питомца"):
        ID_OF_THE_UPDATE_PET = create_and_delete_pet["id"]
        new_info_pet = {
            "id": ID_OF_THE_UPDATE_PET,
            "name": fake.first_name(),
            "status": fake.random_element(elements=('available','sold',"pending")),
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


        req = requests.Request('PUT', f'{PET_SERVICE_URL}/pet', json=new_info_pet)
        prepared = req.prepare()
        headers = [f"{k}: {v}" for k, v in prepared.headers.items()]

        basic_data = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок запроса": headers,
            "Тело запроса": new_info_pet,
        }

        allure.attach(
            json.dumps(basic_data, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )


    
    with allure.step("Отправить запрос для обновления информации и проверить обновление питомца"):
        update_response = requests.put(f'{PET_SERVICE_URL}/pet', json=new_info_pet)
        assert update_response.status_code == 200

        headers_responce = [f"{k}: {v}" for k, v in update_response.headers.items()]
        request_body = json.loads(update_response.text)

        put_responce_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок ответа": headers_responce,
            "Тело ответа": request_body,
            "Статус": update_response.status_code
        }
        
        allure.attach(
        json.dumps(put_responce_server, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
    )
    

    with allure.step("Проверяем,что новый данные можно получить с помощью запроса get"):
        get_response = requests.get(f'{PET_SERVICE_URL}/pet/{ID_OF_THE_UPDATE_PET}')
        assert get_response.status_code == 200
        updated_data = get_response.json()

        METHOD = 'GET'
        headers_str_responce = [f"{k}: {v}" for k, v in get_response.headers.items()]
        request_body = json.loads(get_response.text)

        get_responce_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок ответа": headers_str_responce,
            "Тело ответа": request_body,
            "Статус": get_response.status_code
        }
        
        allure.attach(
        json.dumps(get_responce_server, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
    )
    
    with allure.step("Сравнить ответ с схемой Pet"):
        try:
            validated_pet = Pet(**updated_data)
        except ValidationError as expect:
            assert False

@allure.title('Неверный путь для обновления данных') 
def test_invalid_specified_path_for_update(create_and_delete_pet):
    
    with allure.step("Указать неверный путь"):
        update_response = requests.put(f'{PET_SERVICE_URL}/not_pet', json=create_and_delete_pet)    
    
    with allure.step("Получить ошибку: Питомец не найден"):
        assert update_response.status_code == 404
    


        headers_responce = [f"{k}: {v}" for k, v in update_response.headers.items()]
        request_body = json.loads(update_response.text)

        put_responce_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/not_pet',
            "Заголовок ответа": headers_responce,
            "Тело ответа": request_body,
            "Статус": update_response.status_code
        }
        
        allure.attach(
        json.dumps(put_responce_server, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
    )
    


@allure.title('Неккоректные данные для обновления') 
def test_failed_update_due_to_an_invalid_pet_ID():

    with allure.step("Создаем питомца с неккоректным ID"):
        new_info_pet = {
        "id": 'BC',
        "name": "Cat",
        "status": "sold",
    }
        req = requests.Request('PUT', f'{PET_SERVICE_URL}/pet', json=new_info_pet)
        prepared = req.prepare()
        headers = [f"{k}:{v}" for k, v in prepared.headers.items()]
        basic_data = {
        "Метод запроса": METHOD,
        "Адрес": PET_SERVICE_URL+'/pet',
        "Заголовок запроса": headers,
        "Тело запроса": new_info_pet,
        }

        allure.attach(
        json.dumps(basic_data, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
        )
    
    with allure.step("Получаем ошибку о неверных данных"):
        update_response = requests.put(f'{PET_SERVICE_URL}/pet', json=new_info_pet)    
        assert update_response.status_code == 400


        headers_responce = [f"{k}: {v}" for k, v in update_response.headers.items()]
        request_body = json.loads(update_response.text)

        put_responce_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок ответа": headers_responce,
            "Тело ответа": request_body,
            "Статус": update_response.status_code
        }
        
        allure.attach(
        json.dumps(put_responce_server, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
        )
        

@allure.title('Недопустимая команда обновления данных') 
def test_invalid_request_patch(create_and_delete_pet):
    with allure.step("Используем команду patch,недопустимый метод"):
        METHOD = 'Patch'
        update_response = requests.patch(f'{PET_SERVICE_URL}/pet', json=create_and_delete_pet) 
        
    with allure.step("Получаем статус код о недопустимом HTTP-методе"):
        assert update_response.status_code == 405
              
        headers_responce = [f"{k}: {v}" for k, v in update_response.headers.items()]
        request_body = json.loads(update_response.text)

        put_responce_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок ответа": headers_responce,
            "Тело ответа": request_body,
            "Статус": update_response.status_code
        }
        
        allure.attach(
        json.dumps(put_responce_server, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
        )