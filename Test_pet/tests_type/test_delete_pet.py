import requests
import json
import allure

PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.title("Удаление питомца по ID")       
def test_deleted_pet(create_pet):
    METHOD = 'DELETE'
    with allure.step("Отправляем запрос на удаление по ID питомца"): 
        DELETE_PET_ID = create_pet['id']
        response = requests.delete(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
        
        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]
        get_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+'/pet',
            "Заголовок ответа": headers_response,
            "Тело ответа": response.text,
            "Статус": response.status_code
        }
        
        allure.attach(
            json.dumps(get_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert response.status_code == 200
    
    with allure.step("Проверяем,что питомца больше нельзя найти"): 
        METHOD = 'GET'
        requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{DELETE_PET_ID}')
        headers_response = [f"{k}: {v}" for k, v in requests_response.headers.items()]
        delete_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{DELETE_PET_ID}',
            "Заголовок ответа": headers_response,
            "Тело ответа": requests_response.text,
            "Статус": requests_response.status_code
        }
        
        allure.attach(
            json.dumps(delete_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert requests_response.status_code == 404



@allure.title("Удаление питомца по имени")   
def test_try_delete_pet_by_name(create_pet):
    METHOD = 'DELETE'
    with allure.step("Отправляем запрос на удаление по имени питомца и получаем ошибку"): 
        PET_NAME = create_pet['name']
        TRUE_PET_ID = create_pet['id']

        response = requests.delete(f'{PET_SERVICE_URL}/pet/{PET_NAME}')
        
        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]
        response_body = json.loads(response.text)
        delete_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{PET_NAME}',
            "Заголовок ответа": headers_response,
            "Тело ответа": response_body,
            "Статус": response.status_code
        }
        
        allure.attach(
            json.dumps(delete_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert response.status_code == 400
    
    with allure.step("Отправляем запрос get,чтобы проверить,что питомец остался в базе"): 
        requests_response = requests.get(f'{PET_SERVICE_URL}/pet/{TRUE_PET_ID}')
        METHOD = 'GET'
        headers_response = [f"{k}: {v}" for k, v in requests_response.headers.items()]
        response_body = json.loads(requests_response.text)
        delete_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{TRUE_PET_ID}',
            "Заголовок ответа": headers_response,
            "Тело ответа": response_body,
            "Статус":requests_response.status_code
        }
        
        allure.attach(
            json.dumps(delete_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert requests_response.status_code == 200
