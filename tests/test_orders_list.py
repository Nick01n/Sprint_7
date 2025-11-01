import requests
import allure

BASE_URL = "https://qa-scooter.praktikum-services.ru"
GET_ORDERS_ENDPOINT = f"{BASE_URL}/api/v1/orders"



@allure.feature("Получение списка заказов")
@allure.title("Проверка, что в теле ответа возвращается список заказов")
def test_get_orders_returns_list():

    with allure.step("Отправляем GET-запрос на получение списка заказов без параметров"):
        response = requests.get(GET_ORDERS_ENDPOINT)

    with allure.step("Проверяем, что код ответа равен 200"):
        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

    with allure.step("Проверяем, что в ответе присутствует ключ 'orders'"):
        response_json = response.json()
        assert "orders" in response_json, f"В ответе нет ключа 'orders': {response_json}"

    with allure.step("Проверяем, что 'orders' является списком"):
        assert isinstance(response_json["orders"], list), \
            f"Поле 'orders' должно быть списком, а не {type(response_json['orders'])}"

    with allure.step("Если список не пустой — проверяем структуру первого заказа"):
        if response_json["orders"]:
            first_order = response_json["orders"][0]
            expected_keys = [
                "id", "firstName", "lastName", "address", "metroStation",
                "phone", "rentTime", "deliveryDate", "track", "color", "comment"
            ]
            missing = [key for key in expected_keys if key not in first_order]
            assert not missing, f"В объекте заказа отсутствуют поля: {missing}"
