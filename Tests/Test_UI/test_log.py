import pytest
import allure
from playwright.sync_api import Page, expect 
from pages.recovery_page import RecoveryPage


@allure.title("Проверка вывода ошибки логина или пароля")
def test_login_password_error(login_page):
    
    login_page.check_login_form()

    with allure.step("Ввод неверных значений"):
        login_page.login('login', 'password')
     
    login_page.check_error_message()



@allure.title("Проверка вывода страницы с восстановлением")
def test_three_errors_to_the_recovery_page(login_page,page):
    
    login_page.enter_wrong_password_three_times('login', 'password')
    recovery_page = RecoveryPage(page) 
    recovery_page.check_restore_form()
    

@allure.title("Проверка отображения qr кода")
def test_qr_visibility(login_page):

    login_page.click_and_check_qr()


@allure.title("Проверка перехода на страницу регистрации")
def test_registration_redirect(login_page):

    login_page.click_registration_button()