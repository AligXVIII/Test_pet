import allure


@allure.title("Создание пользователя с неверным id")
def test_create_user_invalid_id(app):
    user_data = app.generate_factory.generate_test_user_data(data_type='invalid_ID')
    post_response = app.api.user.post_user(user_data)
    assert post_response.status_code == 400


@allure.title("Успешный логин пользователя")
def test_user_login_success(app):
    response = app.api.user.get_user_login("user1", "password1")
    assert response.status_code == 200


@allure.title("Логаут пользователя")
def test_user_logout(app):
    response = app.api.user.get_user_logout()
    assert response.status_code == 200


@allure.title("Проверка что удаление пользователей недоступно в API")
def test_user_deletion_not_allowed(app):

    login_response = app.api.user.get_user_login("user1", "password1")
    assert login_response.status_code == 200
    
    get_response = app.api.user.get_user_by_username("user1")
    assert get_response.status_code == 200
    
    delete_response = app.api.user.delete_user("user1")
    assert delete_response.status_code == 500 
    
    check_response = app.api.user.get_user_by_username("user1")
    assert check_response.status_code == 200 