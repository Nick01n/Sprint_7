import pytest
import requests
from utils.helpers import generate_random_string
from utils.URL import BASE_URL



@pytest.fixture
def create_and_delete_courier():
    
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {"login": login, "password": password, "firstName": first_name}
    requests.post(f"{BASE_URL}/courier", json=payload)  # без assert, просто создаем

    yield {"login": login, "password": password, "firstName": first_name}

    # Удаляем курьера после теста
    login_response = requests.post(f"{BASE_URL}/courier/login",
                                   json={"login": login, "password": password})
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{BASE_URL}/courier/{courier_id}")


@pytest.fixture
def create_and_cancel_order():
    """Создает заказ и отменяет его после теста"""
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Test address",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 2,
        "deliveryDate": "2025-10-28",
        "comment": "Test order",
        "color": ["BLACK"]
    }

    create_response = requests.post(f"{BASE_URL}/orders", json=payload)
    order_data = create_response.json()
    track = order_data.get("track")

    yield track

    # Отмена заказа с правильным URL (как указал ревьюер)
    if track:
        requests.put(f"{BASE_URL}/orders/cancel", params={"track": track})
