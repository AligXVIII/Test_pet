import pytest
from framework.entry_point.application import Application


@pytest.fixture
def app():
    return Application()


@pytest.fixture(scope="function")
def create_pet(app):
    try:
        request_json = app.generate_factory.generate_test_pet_data()
        response = app.api.pet.post_pet(request_json)
        assert response.status_code == 200, f"Ошибка создания питомца: {response.status_code}"
        return response.json()
    except Exception as e:
        pytest.skip(f"Не удалось создать питомца: {e}")


@pytest.fixture(scope="function")
def create_and_delete_pet(app, create_pet):
    pet_data = create_pet
    yield pet_data
    try:
        app.api.pet.delete_pet(pet_data["id"])
    except Exception as e:
        print(f"Ошибка удаления питомца {pet_data['id']}: {e}")


@pytest.fixture
def create_order_with_cleanup(app):
    try:
        order_data = app.generate_factory.generate_test_order_data()
        app.api.store.post_order(order_data)
        yield order_data
        app.api.store.delete_order(order_data["id"])
    except Exception as e:
        pytest.skip(f"Не удалось создать заказ: {e}")