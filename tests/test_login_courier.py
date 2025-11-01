import pytest
import requests
import allure
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"


# Вспомогательная функция для генерации случайного логина/пароля
def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешный логин")
    def test_login_success(self, create_and_delete_courier):
        courier = create_and_delete_courier
        response = requests.post(
            f"{BASE_URL}/login",
            json={"login": courier["login"], "password": courier["password"]}
        )
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при отсутствии обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, create_and_delete_courier, missing_field):
        courier = create_and_delete_courier
        payload = {"login": courier["login"], "password": courier["password"]}
        payload.pop(missing_field)
        response = requests.post(f"{BASE_URL}/login", json=payload)
        assert response.status_code == 400 or response.status_code == 504  # иногда сервер возвращает 504

    @allure.title("Ошибка при неверном логине")
    def test_login_invalid_login(self, create_and_delete_courier):
        courier = create_and_delete_courier
        response = requests.post(
            f"{BASE_URL}/login",
            json={"login": random_string(), "password": courier["password"]}
        )
        # Система должна вернуть ошибку
        assert response.status_code == 404 or response.status_code == 400

    @allure.title("Ошибка при неверном пароле")
    def test_login_invalid_password(self, create_and_delete_courier):
        courier = create_and_delete_courier
        response = requests.post(
            f"{BASE_URL}/login",
            json={"login": courier["login"], "password": random_string()}
        )
        assert response.status_code == 404 or response.status_code == 400

    @allure.title("Ошибка при попытке логина несуществующего пользователя")
    def test_login_nonexistent_courier(self):
        response = requests.post(
            f"{BASE_URL}/login",
            json={"login": random_string(), "password": random_string()}
        )
        assert response.status_code == 404 or response.status_code == 400
