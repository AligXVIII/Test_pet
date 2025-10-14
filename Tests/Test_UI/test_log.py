import pytest
import allure
import random
from playwright.sync_api import Page, expect
from pages.page_ok import *
from utils_UI import *


@allure.title("Проверка вывода ошибки логина или пароля")
def test_login_password_error(page: Page):
    with allure.step("Перейти на главную страницу Одноклассников"):
        login_page = LoginPage(page)  
        login_page.open() 

    with allure.step("Проверить видимость страницы входа"):
        login_page.check_login_form()
        login_page.screenshot()

    with allure.step("Ввод неверных значений"):
        
        login = str(random.randint(1, 1000))
        password = str(random.randint(1, 1000))
        login_page.login(login, password)
        allure.attach(
            f"Логин: {login}, Пароль: {password}",
            name="Логин и пароль",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверить видимость ошибки"):
        
        login_page.check_error_message()
        login_page.screenshot()


@allure.title("Проверка вывода страницы с восстановлением")
def test_three_errors_to_the_recovery_page(page: Page):

    login_page=open_login_ok(page)   

    with allure.step("Вводим трижды неверный пароль"):
        
        for i in range(3):
            login_page.login('false_login', 'false_password')
            if i < 2:
                login_page.check_login_form()

    with allure.step("Проверить видимость страницы восстановления"):
        recovery_page = RecoveryPage(page) 
        recovery_page.check_restore_form()
        login_page.screenshot()

    

@allure.title("Проверка отображения qr кода")
def test_qr_visibility(page: Page):

    login_page=open_login_ok(page)   

    with allure.step("Перейти на отображение qr"):
        login_page.click_and_check_qr()
        login_page.screenshot()


@allure.title("Проверка перехода на страницу регистрации")
def test_registration_redirect(page: Page):

    login_page=open_login_ok(page)   

    with allure.step("Переходим на страницу регистрации"):
        login_page.click_and_check_registration()
        login_page.screenshot()