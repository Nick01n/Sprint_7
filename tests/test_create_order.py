import pytest
import requests
import allure

BASE_URL = "https://qa-scooter.praktikum-services.ru"
CREATE_ORDER_ENDPOINT = f"{BASE_URL}/api/v1/orders"


@allure.feature("Создание заказа")
@allure.title("Проверка создания заказа с разными вариантами цвета")
@pytest.mark.parametrize("color",[
    ["BLACK"],
    ["GREY"],
    ["BLACK","GREY"],
    []
])



def test_create_order_with_different_colors(color):
    payload = {
        "firstName": "Nikita",
        "lastName": "Vlasov",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": color
    }
    with allure.step(f"Отправляем запрос на создание заказа с цветом: {color}"):
        response = requests.post(CREATE_ORDER_ENDPOINT, json=payload)

    with allure.step("Проверяем, что код ответа равен 201"):
        assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"
    
    with allure.step("Проверяем, что в ответе есть поле 'track'"):
        response_json = response.json()
        assert "track" in response_json, f"Поле 'track' отсутствует в ответе: {response_json}"
    
    with allure.step("Проверяем, что 'track' имеет числовое значение"):
        track_value = response_json["track"]
        assert isinstance(track_value,int), f"Поле 'track' должно быть числом, а не {type(track_value)}"