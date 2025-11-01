import pytest
import requests
import allure
from utils.URL import BASE_URL

@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self,create_and_delete_courier):
        courier = create_and_delete_courier
        response = requests.post(f"{BASE_URL}/courier/login", json={"login": courier["login"], "password": courier["password"]})
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self,create_and_delete_courier):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"], "firstName": courier["firstName"]}
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 409

    @allure.title("Ошибка при отсутствии обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_required_field(self,create_and_delete_courier, missing_field):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"], "firstName": courier["firstName"]}
        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code == 400

    @allure.title("Проверка корректности кода ответа и тела успешного запроса")
    def test_create_courier_check_status_and_body(self,create_and_delete_courier):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"], "firstName": courier["firstName"]}
        response = requests.post(f"{BASE_URL}/courier", json=payload)
        assert response.status_code in [201, 409]
        if response.status_code == 201:
            assert response.json() == {"ok": True}
