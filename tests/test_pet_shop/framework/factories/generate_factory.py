from faker import Faker
import random
import allure


class GenerateFactory:
    def __init__(self, locale="ru_RU"):
        self.fake = Faker(locale)
    
    @allure.step("Генерация случайного питомца")
    def generate_test_pet_data(self, pet_id=None, data_type="valid"):
        if pet_id is None:
            pet_id = random.randint(1, 1000)
        
        pet = {
            "valid": {
                "id": pet_id,
                "name": self.fake.first_name(),
                "status": self.fake.random_element(elements=("available", "sold", "pending")),
                "category": {"id": 1, "name": "dogs"},
                "tags": [{"id": 1, "name": "vip"}],
                "photoUrls": ["https://example.com/photo.jpg"]
            },
            "invalid_id": {
                "id": "abxc",
                "name": self.fake.first_name(),
                "status": self.fake.random_element(elements=("available", "sold"))
            },
            "empty_name": {
                "id": pet_id,
                "name": "",
                "status": "available"
            }
        }
        
        return pet[data_type]
    



    @allure.step("Генерация заказа в магазине")
    def generate_test_order_data(self, order_id=None, data_type="valid"):
        if order_id is None:
            order_id = random.randint(1, 1000)
    
        order = {
            "valid": {
                "id": order_id,
                "petId": random.randint(1, 1000),
                "quantity": random.randint(1, 10),
                "shipDate": "2024-01-01T00:00:00.000Z",
                "status": self.fake.random_element(elements=("placed", "approved", "delivered")),
                "complete": True
            },
            "invalid": {
                "id": order_id,
                "petId": "invalid_pet_id",
                "quantity": -1,
                "shipDate": "invalid_date",
                "status": "invalid_status",
                "complete": "not_boolean"
            },
        }
    
        return order[data_type]
    


    @allure.step("Генерация пользователя в магазине")
    def generate_test_user_data(self, order_id=None, data_type="valid"):
    
        order = {
            'valid':
                {
                    "id": 99999,
                    "username": "testuser1129090987",
                    "firstName": "John",
                    "lastName": "Doe",
                    "email": "john.doe@example.com", 
                    "password": "12345",
                    "phone": "1234567890",
                    "userStatus": 0
                },
            "invalid_ID": {
                "id": 'hjk',
                "username": self.fake.first_name(),
                "firstName": self.fake.middle_name(),
                "lastName": self.fake.last_name(),
                "email": self.fake.address(),
                "password": self.fake.password(),
                "phone": self.fake.phone_number(),
                "userStatus": 1,
            },
        }
    
        return order[data_type]





