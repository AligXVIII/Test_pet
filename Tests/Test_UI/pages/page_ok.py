from playwright.sync_api import Page,expect
from pages.base_page import BasePage

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

    def click_and_check_registration(self):
        self.registration_button.click()
        expect(self.page).to_have_url("https://ok.ru/dk?st.cmd=anonymRegistrationEnterPhone")
    
    
    def check_login_form(self):
        expect(self.username_field).to_be_visible()
        expect(self.password_field).to_be_visible() 
        expect(self.login_button).to_be_visible()

    def click_and_check_qr(self):
        self.qr_button.click()
        expect(self.qr_png).to_be_visible()


    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()


    def check_error_message(self):
        expect(self.login_error).to_be_visible()
        expect(self.login_error).to_have_text('Неправильно указан логин и/или пароль')
    

class RecoveryPage(BasePage):
    
    def __init__(self, page,):
        super().__init__(page,'https://ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong&st.email=f')
        self.restore_field = page.locator('[class="button-pro __wide mb-3x"]')
        self.error_message_field = page.locator('[class="stub"]')
        self.return_field =  page.locator('[ data-l="t,cancel" ]')


    def check_restore_form(self):
        expect(self.restore_field).to_be_visible()
        expect(self.error_message_field).to_be_visible() 
        expect(self.return_field).to_be_visible()
