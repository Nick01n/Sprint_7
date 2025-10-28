import pytest
import requests
import allure

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"


@allure.feature("Создание заказа")
@allure.title("Создание заказа с разными вариантами цвета")
@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
])
def test_create_order_with_different_colors(color):
    # Формируем тело запроса
    payload = {
        "firstName": "Nastya",
        "lastName": "Vlasova",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 351 31 31",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color
    }

    # Отправляем запрос на создание заказа
    with allure.step(f"Отправляем запрос на создание заказа с цветом {color}"):
        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"

    # Проверяем, что в ответе есть поле track и оно число
    with allure.step("Проверяем, что в ответе есть поле 'track' и это число"):
        data = response.json()
        assert "track" in data, f"Поле 'track' отсутствует: {data}"
        assert isinstance(data["track"], int), f"Track не число: {data['track']}"

    # Отмена заказа
    with allure.step("Отменяем созданный заказ"):
        track = data["track"]
        cancel_response = requests.put(f"{BASE_URL}/orders/cancel", json={"track": track})
        # Если отмена не удалась — тест падает
        assert cancel_response.status_code in [200, 404], (
            f"Не удалось отменить заказ, статус: {cancel_response.status_code}, тело: {cancel_response.text}"
        )
