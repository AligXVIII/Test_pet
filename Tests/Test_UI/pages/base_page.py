from playwright.sync_api import Page
import allure

class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def open(self, path: str = ""):
        self.page.goto(f"{self.base_url}/{path}")

    def screenshot(self, path: str = ""):
        allure.attach(
            self.page.screenshot(),
            name="Скриншот",
            attachment_type=allure.attachment_type.PNG
        )