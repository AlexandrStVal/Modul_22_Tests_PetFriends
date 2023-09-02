"""ХРАНЕНИЕ ФИКСТУР"""
# import pytest
#
# winner_names = []
#
# @pytest.fixture
# def add_winner_names():
#     names = 'Bob Kate Jake Smit'
#     for name in names.split(" "):
#         winner_names.append(name)
#
# @pytest.fixture
# def name():
#     print('\n\n Test Started')
#     yield 'Kate'
#     print('\n\n Test finished')
#
#
# @pytest.fixture(autouse=True)
# def time_out():
#     start_time = datetime.datetime.now()
#     yield
#     end_time = datetime.datetime.now()
#     print(f"\nТест шел: {end_time - start_time}")

'''Modul 21 for test_pet_friends.py'''
import pytest
import datetime
from settings import valid_email, valid_password
from api import PetFriends
import requests

pf = PetFriends()


# Task 22.2
# Pre-request
# autouse=True - для автоматической отработки
# scope="class" - запускается для каждого тестового класса

@pytest.fixture(scope="class", autouse=True)
def auth_key():
    """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email=valid_email, password=valid_password)

    # Сверяем полученные данные по auth_key с нашими ожиданиями
    assert 'key' in result
    assert status == 200
    print(f'\n\nStatus code auth_key: {status}')
    print('\n', result)

    yield result

    # Проверяем что статус ответа = 200
    assert status == 400


# Фикстура request даёт доступ и к другой полезной информации, которая позволяет лучше управлять
@pytest.fixture(autouse=True)  # не работает со scope='class'
def request_fixture(request):
    if 'Pet' in request.function.__name__:
        print(f"\nЗапущен тест {request.function.__name__} из сьюта Дом Питомца")
    if 'get' in request.function.__name__:
        print(f"Запущен тест {request.function.__name__} c методом GET", '\n')
    print('Test name: ', request.function.__name__)
    # print(request.fixturename)   # название фикстуры
    print('Scope: ', request.scope)
    print('Class name: ', request.cls)
    print('Module name: ', request.module.__name__)
    print('File path: ', request.fspath)
    if request.cls:  # почему-то не работает
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"


# Post-request
@pytest.fixture(autouse=True)
def time_out():
    start_time = datetime.datetime.now()
    yield
    end_time = datetime.datetime.now()
    print(f"\nВремя, затраченное на тест: {end_time - start_time}")


# фикстура по заданию 21.6.4
@pytest.fixture(scope='class')
def api_client():
    session = requests.Session()
    response = pf.api_request(session, 'GET', f'{pf.base_url}api/key',
                              headers_update={
                                  'email': valid_email,
                                  'password': valid_password
                              })
    access_token = response.json().get('key')
    assert access_token is not None
    session.headers.update({
        'auth_key': access_token,
        'accept': 'application/json'
    })

    yield session

    print('logout')
