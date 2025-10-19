import pytest
import requests
import allure
from utils.generator import register_new_courier_and_return_login_password

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_couier_success(self):
        payload = {
            "login": "courier_test_3",
            "password": "123456",
            "firstName": "Ivannn"
        }
        with allure.step("Отправляем POST-запрос на создание курьера"):
            response = requests.post(BASE_URL, json=payload)
        
        with allure.step("Проверяем, что код ответа 201 и ответ содержит {'ok': True}"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_dublicate_courier(self):
        payload = {
            "login": "duplicate_user2",
            "password": "123456",
            "firstName": "Alexxx"
        }
        with allure.step("Создаём первого курьера"):
            requests.post(BASE_URL, json=payload)
        with allure.step("Создаём второго с тем же логином"):
            response = requests.post(BASE_URL, json=payload)

        with allure.step("Проверяем, что возвращается ошибка 409"):
            assert response.status_code == 409
            assert response.json()["message"] == "Этот логин уже используется"

    @allure.title("Ошибка при отсутствии обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_required_field(self, missing_field):
        payload = {
            "login": "test_missing_field_1",
            "password": "123456",
            "firstName": "BoB"
        }
        payload.pop(missing_field)

        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            response = requests.post(BASE_URL, json=payload)

        with allure.step("Проверяем, что вернулся код 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Проверка корректности кода ответа и тела успешного запроса")
    def test_create_courier_check_status_and_body(self):
        payload = {
            "login": "status_test_user_1",
            "password": "123456",
            "firstName": "Masha"
        }
        with allure.step("Отправляем POST-запрос"):
            response = requests.post(BASE_URL, json=payload)
        with allure.step("Проверяем код и тело ответа"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}
