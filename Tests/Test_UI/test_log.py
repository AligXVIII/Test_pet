import pytest
import allure
import random
from playwright.sync_api import Page, expect
from Pages.main_page_ok import LoginPage 


@allure.title("Проверка вывода ошибки логина или пароля")
def test_ok_main_page(page: Page):
    with allure.step("Перейти на главную страницу Одноклассников"):
        login_page = LoginPage(page)  
        login_page.navigator()

    with allure.step("Проверить видимость страницы входа"):
        expect(login_page.username_field).to_be_visible()
        expect(login_page.password_field).to_be_visible()
        expect(login_page.login_button).to_be_visible()

        allure.attach(
            page.screenshot(),
            name="Скриншот",
            attachment_type=allure.attachment_type.PNG
        )

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
        expect(login_page.login_error).to_be_visible()
        expect(login_page.login_error).to_have_text('Неправильно указан логин и/или пароль')

        allure.attach(
            page.screenshot(),
            name="Скриншот",
            attachment_type=allure.attachment_type.PNG
        )