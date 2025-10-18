from playwright.sync_api import Page,expect
import allure
import re
from pages.base_page import BasePage

class RecoveryPage(BasePage):
    
    def __init__(self, page,):
        super().__init__(page,'https://ok.ru')
        self.restore_field = page.locator('[class="button-pro __wide mb-3x"]')
        self.error_message_field = page.locator('[class="stub"]')
        self.return_field =  page.locator('[ data-l="t,cancel" ]')


    @allure.step("Проверить видимость страницы восстановления")
    def check_restore_form(self):
        expect(self.page).to_have_url(re.compile(r".*st.accRecovery=on.*"))
        expect(self.restore_field).to_be_visible()
        expect(self.error_message_field).to_be_visible() 
        expect(self.return_field).to_be_visible()
        self.screenshot('Страница восстановления')
