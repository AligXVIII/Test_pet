import pytest
from playwright.sync_api import Page, expect
import allure

@allure.title("Проверка поисковой строки Google")
def test_google_search_box(page: Page):
    
    with allure.step("Перейти на главную страницу Google"):
        
        page.goto("https://www.google.com")

    with allure.step("Найти поисковую строку"):

        search_box = page.get_by_role("combobox", name="Найти")


    with allure.step("Проверить видимость поисковой строки"):
        expect(search_box).to_be_visible()

        allure.attach(
            page.screenshot(),
            name="Скриншот",
            attachment_type=allure.attachment_type.PNG
        )