import allure
from constants import  NONEXISTENT_ID

@allure.title("Поиск заказа на покупку по ID")
def test_successful_get_store_id(app,create_order_with_cleanup):

   get_response = app.api.store.get_order(create_order_with_cleanup["id"])
   assert get_response.status_code == 200



@allure.title("Поиск заказа на покупку по несуществующему ID")
def test_get_nonexistent_order_id(app,):
    
   get_response = app.api.store.get_order(NONEXISTENT_ID)
   assert get_response.status_code == 404


@allure.title("Поиск заказа на покупку по дате")
def test_get_order_by_invalid_parameter(app,create_order_with_cleanup):
    
   get_response = app.api.store.get_order(create_order_with_cleanup['shipDate'])
   assert get_response.status_code == 400


@allure.title("Получение инвентаря магазина")
def test_get_store_inventory(app):

   get_response = app.api.store.get_inventory()
   assert get_response.status_code == 200

   order_data = app.generate_factory.generate_test_order_data()
   app.api.store.post_order(order_data)

   get_response = app.api.store.get_inventory()
   assert get_response.status_code == 200

   inventory = get_response.json()
   assert isinstance(inventory, dict)
   assert all(isinstance(count, int) for count in inventory.values())