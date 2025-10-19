import pytest
import requests
import allure
from utils.generator import register_new_courier_and_return_login_password

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier/login"


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Курьер может авторизоваться (успешный логин)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_courier_success(self):
        creds = register_new_courier_and_return_login_password()
        login,password,_ = creds

        payload = {
            "login": login,
            "password": password
        }

        with allure.step("Отправляем POST-запрос для авторизации"):
            response = requests.post(BASE_URL, json=payload)

        with allure.step("Проверяем, что возвращается id и статус-код 200"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Ошибка при неправильном логине или пароле")
    def test_login_with_wrong_credentials(self):
        payload = {
            "login": "wrong_login",
            "password": "wrong_pass"
        }
        with allure.step("Отправляем POST-запрос с неверными данными"):
            response = requests.post(BASE_URL, json=payload)
        with allure.step("Проверяем, что статус 404 и сообщение об ошибке"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.json()["message"]

    @allure.title("Ошибка при отсутствии обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field(self, missing_field):
        
        creds = register_new_courier_and_return_login_password()
        login, password, _ = creds
        payload = {"login": login, "password": password}
        payload.pop(missing_field)

        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            response = requests.post(BASE_URL, json=payload)

        with allure.step("Проверяем, что код 400 и сообщение о недостаточных данных"):
            assert response.status_code == 400
            assert "Недостаточно данных" in response.json()["message"]

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_non_existing_user(self):
       
        payload = {
            "login": "non_existing_user",
            "password": "qwerty12345"
        }

        with allure.step("Отправляем запрос для несуществующего пользователя"):
            response = requests.post(BASE_URL, json=payload)

        with allure.step("Проверяем, что возвращается 404 и сообщение 'Учетная запись не найдена'"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.json()["message"]