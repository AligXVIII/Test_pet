import pytest
from pages.page_ok import LoginPage

@pytest.fixture
def login_page(page):
    login_page = LoginPage(page)
    login_page.open_main_page()
    return login_page