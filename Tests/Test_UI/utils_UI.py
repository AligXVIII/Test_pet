import pytest
import allure
from playwright.sync_api import Page, expect
from pages.page_ok import *


def open_login_ok(page: Page):
    with allure.step("Перейти на главную страницу Одноклассников"):
        login_page = LoginPage(page)  
        login_page.open()
        login_page.screenshot()
    return login_page   
