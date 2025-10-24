import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@pytest.fixture
def base_url():
    return BASE_URL


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture
def create_and_delete_courier():
    
    login = generate_random_string()
    password = generate_random_string()
    firstName = generate_random_string()

    payload = {"login": login, "password": password, "firstName": firstName}
    response = requests.post(f"{BASE_URL}/courier", json=payload)
    assert response.status_code in [201, 409], f"Ошибка при создании курьера: {response.text}"

    yield {"login": login, "password": password, "firstName": firstName}

    # Попробуем удалить курьера
    login_resp = requests.post(f"{BASE_URL}/courier/login", json={"login": login, "password": password})
    if login_resp.status_code == 200:
        courier_id = login_resp.json()["id"]
        requests.delete(f"{BASE_URL}/courier/{courier_id}")


@pytest.fixture
def create_and_cancel_order():
    
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Temporary order",
        "color": ["BLACK"]
    }

    response = requests.post(f"{BASE_URL}/orders", json=payload)
    assert response.status_code == 201, f"Ошибка при создании заказа: {response.text}"
    track = response.json()["track"]

    yield track

    # Отмена заказа
    cancel_response = requests.put(f"{BASE_URL}/orders/cancel", json={"track": track})
    assert cancel_response.status_code in [200, 404], (
        f"Не удалось отменить заказ, статус: {cancel_response.status_code}, тело: {cancel_response.text}"
    )
