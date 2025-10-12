from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_field = page.locator('#field_email')
        self.password_field = page.locator('#field_password')
        self.login_button = page.locator('[data-l="t,sign_in"]')
        self.login_error = page.locator('[class="input-e login_error"]')


    def navigator(self):
        self.page.goto('https://ok.ru/')
    

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
