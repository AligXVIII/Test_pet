import allure
import json
import requests

def log_response(response):
    method = response.request.method if response.request else "UNKNOWN"
    url = response.request.url if response.request else "UNKNOWN"

    try:
        response_body = json.loads(response.text) if response.text else "(пустой ответ)"
    except json.JSONDecodeError:
        response_body = response.text
    
    log_data = {
        "Метод запроса": method,
        "Адрес": url,
        "Заголовок ответа": [f"{k}: {v}" for k, v in response.headers.items()],
        "Тело ответа": response_body,
        "Статус": response.status_code
    }
    
    allure.attach(
        json.dumps(log_data, ensure_ascii=False, indent=2),
        "Response log",
        allure.attachment_type.JSON
    )
    
    return response


def log_request(METHOD, URL, request):
    
    temp_req = requests.Request(METHOD, URL, json=request)
    prepared = temp_req.prepare()
    
    request_data = {
        "Метод запроса": METHOD,
        "Адрес": URL,
        "Заголовок запроса": [f"{k}: {v}" for k, v in prepared.headers.items()],
        "Тело запроса": request,
    }
    
    allure.attach(
        json.dumps(request_data, ensure_ascii=False, indent=2),
        "Request log",
        allure.attachment_type.JSON
    )