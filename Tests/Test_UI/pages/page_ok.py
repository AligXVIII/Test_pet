from playwright.sync_api import Page,expect
from pages.base_page import BasePage
import allure
import re
class LoginPage(BasePage):

    def __init__(self, page,):
        super().__init__(page,'https://ok.ru')
        self.username_field = page.locator('#field_email')
        self.password_field = page.locator('#field_password')
        self.login_button = page.locator('[data-l="t,sign_in"]')
        self.login_error = page.locator('[class="input-e login_error"]')
        self.qr_button = page.locator('[data-l="t,qr_tab"]')
        self.qr_png = page.locator('[class="qr_code_image"]')
        self.registration_button= page.locator ('[class="button-pro __sec mb-3x __wide"]') 


    @allure.step("Переходим на страницу регистрации")
    def click_registration_button(self):
        self.registration_button.click()
        expect(self.page).to_have_url(re.compile(r".*st\.cmd=anonymRegistration.*"))    
        self.screenshot("Страница регистрации")
    
    
    @allure.step("Проверить видимость страницы входа")   
    def check_login_form(self):
        expect(self.username_field).to_be_visible()
        expect(self.password_field).to_be_visible() 
        expect(self.login_button).to_be_visible()
        self.screenshot("Форма логина")


    @allure.step("Перейти на отображение qr")
    def click_and_check_qr(self):
        self.qr_button.click()
        expect(self.qr_png).to_be_visible()
        self.screenshot("QR код")

    @allure.step("Ввод логина и пароля")
    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()


    @allure.step("Ввести неверный пароль 3 раза")
    def enter_wrong_password_three_times(self,false_username, false_password):
        for i in range(3):
            self.login(false_username, false_password)
            if i < 2:
                expect(self.username_field).to_be_visible()
                expect(self.password_field).to_be_visible() 
                expect(self.login_button).to_be_visible()



    @allure.step("Проверить видимость ошибки")
    def check_error_message(self):
        expect(self.login_error).to_be_visible()
        expect(self.login_error).to_have_text('Неправильно указан логин и/или пароль')
        self.screenshot("Ошибка логина")


    @allure.step("Перейти на главную страницу Одноклассников")
    def open_main_page(self):
        self.open()
        self.screenshot("Главная страница")
        return self

    

