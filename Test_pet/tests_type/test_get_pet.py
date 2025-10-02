import requests
import json
import allure
PET_SERVICE_URL = 'http://5.181.109.28:9090/api/v3'
METHOD = 'GET'

@allure.title("Получение информации о питомце по ID")   
def test_successful_get_pet_id(create_and_delete_pet):
    with allure.step("Задаем ID питомца,информацию о котором мы хотим узнать"): 
        pet_id = create_and_delete_pet['id']
        allure.attach(
            f"ID: {pet_id}",
            "ID питомца",
            allure.attachment_type.TEXT
        )

    with allure.step("Отправляем запрос get и проверяем успешность запроса"): 
        response = requests.get(f'{PET_SERVICE_URL}/pet/{pet_id}')
        response_json = response.json()
        
        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]
        response_body = json.loads(response.text)
        get_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{pet_id}',
            "Заголовок ответа": headers_response,
            "Тело ответа": response_body,
            "Статус": response.status_code
        }
        
        allure.attach(
            json.dumps(get_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert response.status_code == 200

    with allure.step("Проверяем,что имя питомца,которого мы создали совпадает с полученной информацией от запроса"): 
        assert create_and_delete_pet['name'] == response_json['name']


@allure.title("Неудачное получение информации о питомце по имени")   
def test_get_by_name_and_check_failed(create_and_delete_pet):
 
    with allure.step("Задаем имя,по которому будем искать информацию"): 
        pet_name = create_and_delete_pet['name']
        allure.attach(
            f'Имя: {pet_name}',
            "Имя питомца",
            allure.attachment_type.TEXT
        )

    with allure.step("Получаем ошибку, что сервер не смог обработать запрос"): 
        response = requests.get(f'{PET_SERVICE_URL}/pet/{pet_name}')

        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]
        response_body = json.loads(response.text)
        get_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{pet_name}',
            "Заголовок ответа": headers_response,
            "Тело ответа": response_body,
            "Статус": response.status_code
        }
       
        allure.attach(
            json.dumps(get_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert response.status_code == 400


@allure.title("Неудачное получение информации о питомце с несуществующим ID")   
def test_get_pet_by_nonexistent_id():

    with allure.step("Задаем ID,которого нет в базе"):
        nonexistent_id = 999999999
        allure.attach(
            f'{nonexistent_id}',
            "Заданный ID",
            allure.attachment_type.TEXT
        ) 

    with allure.step("Отправляем запрос на несуществующий ID и получаем ошибку:Питомец не найден"):
        response = requests.get(f'{PET_SERVICE_URL}/pet/{nonexistent_id}')
        
        headers_response = [f"{k}: {v}" for k, v in response.headers.items()]
        #response_body = json.loads(response.text)
        get_response_server = {
            "Метод запроса": METHOD,
            "Адрес": PET_SERVICE_URL+f'/pet/{nonexistent_id}',
            "Заголовок ответа": headers_response,
            "Тело ответа": response.text,
            "Статус": response.status_code
        }

        allure.attach(
            json.dumps(get_response_server, ensure_ascii=False, indent=2),
            "Request log",
            allure.attachment_type.JSON
        )
        assert response.status_code == 404