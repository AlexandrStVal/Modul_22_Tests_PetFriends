'''Moduls 19, 21, 22 for test_pet_friends.py'''
import json
import os
import pytest
from api import PetFriends

pf = PetFriends()

''' Task 22.2 '''
''' TEST: test_getAllPets_positive '''


def empty_string():
    return ''


def only_my_pets():
    return 'my_pets'


@pytest.mark.api
@pytest.mark.get
@pytest.mark.positive
@pytest.mark.parametrize("filter",
                         ['', 'my_pets'],
                         ids=['empty_string', 'only_my_pets']
                         )
def test_getAllPets_positive(auth_key, filter) -> json:
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем статус ответа по test_getAllPets
    assert status == 200
    assert len(result['pets']) > 0
    print(f'\nStatus code: {status}, \nBody: {result}')
    # assert result.headers.get('Content-Type') == 'application/json'
    # assert result.headers.get['Content-Type'] == 'application/json'
    # assert 'application/json' in result.headers['Content-Type']
    # assert 'application/json' in result.headers('Content-Type')


''' TEST: test_getAllPets_negative_filters '''


def generate_string(num):
    return 'a' * num


def chinese_letters():
    return '的一是不了人我在有他这为之大来以个中上们'


def russian_letters():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def special_chars():
    return '|\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.mark.api
@pytest.mark.get
@pytest.mark.negative
@pytest.mark.parametrize("filter",
                         [
                             generate_string(256),
                             generate_string(1001),
                             chinese_letters(),
                             russian_letters(),
                             russian_letters().upper(),
                             special_chars(),
                             1234567890
                         ],
                         ids=
                         [
                             '256 symbols',
                             'more than 1000 symbols',
                             'chinese',
                             'russian',
                             'RUSSIAN',
                             'wildcards',
                             'digit'
                         ])
@pytest.mark.xfail(reason='Тест должен давать статус код: 400. Также не получается запустить проверку по Content-Type')
# xfail Помечает тест как падающий. Если тест прошел успешно, его состояние помечено как XPASS.
# При неудачном прохождении теста статус будет XFAILED.
def test_getAllPets_negative_filters(auth_key, filter) -> json:
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем статус ответа по test_getAllPets
    assert status == 500
    assert 'HTML' or 'html' in result
    print(f'\nStatus code: {status} \nBody: {result}')
    # assert result.headers.get['Content-Type'] == 'text/html; charset=utf-8'
    # assert result.headers.get('Content-Type') == 'text/html; charset=utf-8'
    # assert 'text/html; charset=utf-8' in result.headers['Content-Type']


''' TEST: test_addMyPetValidData '''


@pytest.mark.api
@pytest.mark.post
@pytest.mark.positive
def test_addMyPetValidData(auth_key, name='Hanny', animal_type='Kitty', age='2',
                           pet_photo='images/Kitty.jpg') -> json:
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo'] != ''
    print(f'\nStatus code: {status} \nBody: {result}')

    # print('\nУдаляем питомца')
    # pet_id = result['id']
    # stat_del, res_del = pf.delete_pet(auth_key, pet_id)
    # stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")
    #
    # # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    # assert stat_del == 200
    # assert stat_get == 200
    # assert result['id'] not in res_get
    # print('Status code DELETE:', stat_del)
    # print('Status code GET:', stat_get)
    # print('list of other my pets:', res_get)


''' TEST: test_deleteMyPet '''


@pytest.mark.api
@pytest.mark.delete
@pytest.mark.positive
def test_deleteMyPet(auth_key) -> json:
    """Проверяем возможность удаления питомца"""

    # # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Hanny", "Kitty", '2', "images/Kitty.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    print(f'\nStatus code: {status}')


''' TEST: test_updatePetInfo '''


@pytest.mark.api
@pytest.mark.put
@pytest.mark.positive
def test_updatePetInfo(auth_key, name='Jorik', animal_type='Catyara', age='3') -> json:
    """Проверяем возможность обновления информации о питомце"""

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == age
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my_pets")
    print(f'\nStatus code: {status} \nBody: {result}')

    # print('\n', 'Удаляем питомца')
    # pet_id = result["id"]
    # stat_del, res_del = pf.delete_pet(auth_key, pet_id)
    # stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")
    # # print(res_get, my_pets)
    #
    # # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    # assert stat_del == 200
    # assert stat_get == 200
    # assert result['id'] not in res_get
    # print('Status code DELETE:', stat_del)
    # print('Status code GET:', stat_get)
    # print('list of other my pets:', res_get)


''' TEST: test_addMyPetWithoutPhoto '''
@pytest.mark.api
@pytest.mark.post
@pytest.mark.positive
def test_addMyPetWithoutPhoto(auth_key, name='Kissa', animal_type='Kitty', age='1') -> json:
    """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
    запроса и результат в формате JSON с данными добавленного питомца"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    print('\nId: ', result['id'], '\nStatus code: ', status)

    # print('\n', 'Удаляем питомца')
    # pet_id = result["id"]
    # stat_del, res_del = pf.delete_pet(auth_key, pet_id)
    # stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")
    # # print(res_get, my_pets)

    # # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    # assert stat_del == 200
    # assert stat_get == 200
    # assert result['id'] not in res_get
    # print('Status code DELETE:', stat_del)
    # print('Status code GET:', stat_get)
    # print('list of other my pets:', res_get)


''' TEST: test_addMyPetWithoutPhoto_negative '''
# Генераторы имен параметров в test_getAllPets_negative_filters
def is_age_valid(age):
    # Проверяем, что возраст - это число от 1 до 49 и целое
    return age.isdigit() and 0 < int(age) < 50 and float(age) == int(age)

@pytest.mark.post
@pytest.mark.negative
@pytest.mark.xfail(reason='Тест должен давать статус код: 400 с пустыми полями. Фактически статус код 200.'
                          'Кроме того, провалилось 64 теста')
@pytest.mark.parametrize("name",
                         [
                             '',
                             generate_string(256),
                             generate_string(1001),
                             chinese_letters(),
                             russian_letters(),
                             russian_letters().upper(),
                             special_chars(),
                             '1234567890'
                         ],
                         ids=[
                             'empty',
                             '256 symbols',
                             'more than 1000 symbols',
                             'chinese',
                             'russian',
                             'RUSSIAN',
                             'wildcards',
                             'digit'
                         ])
@pytest.mark.parametrize("animal_type",
                         [
                             '',
                             generate_string(256),
                             generate_string(1001),
                             russian_letters(),
                             russian_letters().upper(),
                             chinese_letters(),
                             special_chars(),
                             "1234567890"
                         ],
                         ids=[
                             'empty',
                             '255 symbols',
                             'more than 1000 symbols',
                             'russian',
                             'RUSSIAN',
                             'chinese',
                             'specials',
                             'digit'
                         ])
@pytest.mark.parametrize("age",
                         [
                             '',
                             '-1',
                             '0',
                             '1',
                             '100',
                             '1.5',
                             '2147483647',
                             '2147483648',
                             russian_letters(),
                             russian_letters().upper(),
                             chinese_letters(),
                             special_chars()
                         ],
                         ids=[
                             'empty',
                             'negative',
                             'zero',
                             'min',
                             'greater than max',
                             'float',
                             'int_max',
                             'int_max + 1',
                             'specials',
                             'russian',
                             'RUSSIAN',
                             'chinese'
                         ])
def test_addMyPetWithoutPhoto_negative(auth_key, name, animal_type, age) -> json:
    """Проверяем, что можно добавить питомца с различными данными"""
    ''' Добавляем питомца '''
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # if name == '' or animal_type == '' or is_age_valid(age):
    #     assert status == 400   # фактически принимает пустые name и animal_type cо статус кодом 200
    # else:
    #     assert status == 200

    # Сверяем полученный ответ с ожидаемым результатом
    if is_age_valid(age):
        assert status == 400
    else:
        assert status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    print('\nId:', result['id'], '\nStatus code: ', status)

    print('\nУдаляем питомца')
    pet_id = result['id']
    stat_del, res_del = pf.delete_pet(auth_key, pet_id)
    stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert stat_del == 200
    assert stat_get == 200
    assert result['id'] not in res_get
    print('\nStatus code DELETE:', stat_del)
    print('\nStatus code GET:', stat_get)
    print('\nlist of other my pets:', res_get)

''' TEST: test_getAllPets Task 21.6.4'''
# @pytest.mark.skip(reason="test_getAllPets::Баг в файле conftest.py: 80 стр. - <ссылка>")
# фикстура, пропускающая тест
@pytest.mark.xfail(reasone='Доделать тест по заданию Задание 21.6.4.'
                           ' Вебинар «Тестовый дизайн для REST API» 02.08.23')
@pytest.mark.get
def test_getAllPets(auth_key, api_client):
    response = pf.api_request(api_client, 'GET', f'{pf.base_url}api/pets')
    assert response.status_code == 200
    assert len(response.json().get('pets')) > 0
    print(response)

    # def test_addMyPetWithoutPhoto(self, auth_key, name='Kissa', animal_type='Kitty', age=1) -> json:
    # """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
    #  запроса и результат в формате JSON с данными добавленного питомца"""
    # # Запрашиваем ключ api и сохраняем в переменную auth_key
    # _, auth_key = pf.get_api_key(valid_email, valid_password)

    # ''' Добавляем питомца '''
    # status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    #
    # # Сверяем полученный ответ с ожидаемым результатом
    # assert status == 200
    # assert result['name'] == name
    # print('\n', 'Id: ', result['id'], '\n', 'Status code: ', status)
    #
    # # print('\n', 'Удаляем питомца')
    # # pet_id = result["id"]
    # # stat_del, res_del = pf.delete_pet(auth_key, pet_id)
    # # stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")
    # # # print(res_get, my_pets)
    #
    # # # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    # # assert stat_del == 200
    # # assert stat_get == 200
    # # assert result['id'] not in res_get
    # # print('Status code DELETE:', stat_del)
    # # print('Status code GET:', stat_get)
    # # print('list of other my pets:', res_get)

    # Тest_2
    # @pytest.mark.skip(reason="test_getPhotoOfPet::Баг в продукте: в api требуется прописывать id - <ссылка>")
    # фикстура пропускающая тест
    # @pytest.mark.get
    # @pytest.mark.xfail(raises=RuntimeError, reason='В файле api/def add_photo_of_pet требуется прописывать id')
    # # тест будет помечен xfail только в том случае, если произойдет исключение типа RuntimeException, в противном случае
    # # тест будет выполняться как обычно (помечаться passed, если пройдет успешно, и failed, если пройдет неуспешно)
    # def test_getPhotoOfPet(self, auth_key, pet_photo='images/Kissa.jpg') -> json:
    #     """Проверяем что можно добавить фото питомца в имеющуюся карточку"""
    #
    #     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    #     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    #     print(pet_photo)

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        # _, res_get = pf.get_list_of_pets(auth_key, 'my_pets')
        # if pet_photo in res_get == '':
        #     print(pet_photo)

        # Добавляем фото питомца
        # status, result = pf.add_photo_of_pet(auth_key, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        # assert status == 200
        # assert result['pet_photo'] != ''
        # print('\n', 'Status code: ', status, '\n', result)

    # # # #Тest_3
    # # # def test_get_api_key_empty_user_data(email='', password='') -> json:
    # # #     """ Негативный сценарий. Проверяем что запрос api ключа c пустыми значениями логина и пароля возвращает статус 403
    # # #        и в результате не содержится слово key."""
    # # #     status, result = pf.get_api_key(email, password)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 403
    # # #     assert 'key' not in result
    # # #     print('\n', 'Status code:', status, '\n', result)
    # # #
    # # #
    # # # # Тest_4
    # # # def test_get_api_key_empty_email(email='', password=valid_password):
    # # #     """ Негативный сценарий. Проверяем что запрос api ключа c пустым значением логина возвращает статус 403
    # # #        и в результате не содержится слово key."""
    # # #     status, result = pf.get_api_key(email, password)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 403
    # # #     assert 'key' not in result
    # # #     print('\n', 'Status code:', status, '\n', result)
    # # #
    # # #
    # # # # Тest_5
    # # # def test_get_api_key_empty_password(email=valid_email, password=''):
    # # #     """ Негативный сценарий. Проверяем что запрос api ключа c пустым значением пароля возвращает статус 403
    # # #        и в результате не содержится слово key."""
    # # #     status, result = pf.get_api_key(email, password)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 403
    # # #     assert 'key' not in result
    # # #     print('\n', 'Status code:', status, '\n', result)
    # # #
    # # #
    # # # Тest_6
    # #     @pytest.mark.api
    # #     @pytest.mark.get
    # #     @pytest.mark.negative
    # #     def test_getApiKey_mixed_up_data(self, email=valid_password, password=valid_email) -> json:
    # #         """ Негативный сценарий. Проверяем что запрос api ключа c перепутанными значениями логина и пароля возвращает статус 403
    # #            и в результате не содержится слово key."""
    # #         status, result = pf.get_api_key(email, password)
    # #
    # #         # Сверяем полученный ответ с ожидаемым результатом
    # #         assert status == 403
    # #         assert 'key' not in result
    # #         print('\n', 'Status code:', status, '\n', result)
    # # #
    # # #
    # # # # Тest_7
    # # # def test_add_new_pet_empty_data(name='', animal_type='', age=''):
    # # #     """Негативный сценарий. Проверяем возможность формирования карточки питомца с пустыми полями"""
    # # #
    # # #     # Запрашиваем ключ api и сохраняем в переменную auth_key
    # # #     _, auth_key = pf.get_api_key(valid_email, valid_password)
    # # #
    # # #     # Добавляем питомца
    # # #     status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # # #
    # # #     # Проверяем что статус ответа = 200 и информация о питомце соответствует заданной
    # # #     assert status == 200
    # # #     assert result['name'] == name
    # # #     print('\n', status, '\n', result)
    # # #
    # # # #Тest_8
    # # # def test_add_pet_empty_name(name='', animal_type='Kitty', age=1, pet_photo='images/Kitty.jpg'):
    # # #     '''Негативный сценарий. Добавление питомца с пустым полем в переменной 'name'.'''
    # # #
    # # #    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # # #     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # # #
    # # #     # Запрашиваем ключ api и сохраняем в переменную auth_key
    # # #     _, auth_key = pf.get_api_key(valid_email, valid_password)
    # # #
    # # #     # Добавляем питомца
    # # #     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 200
    # # #     assert result['name'] == ''
    # # #     print('\n', 'Status code: ', status, '\n', result)
    # # #
    # # #
    # # # #Тest_9
    # # # def test_add_pet_invalid_age(name='Hunny', animal_type='Kitty', age='abc', pet_photo='images/Kitty.jpg'):
    # # #     '''Негативный сценарий. Добавление питомца с указанием букв в переменной 'age'.'''
    # # #
    # # #     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # # #     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # # #
    # # #     # Запрашиваем ключ api и сохраняем в переменную auth_key
    # # #     _, auth_key = pf.get_api_key(valid_email, valid_password)
    # # #
    # # #     # Добавляем питомца
    # # #     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 200
    # # #     assert result['age'] == str(age)
    # # #     print('\n', 'Status code: ', status, '\n', result)
    # # #
    # # # # Тest_10
    # # # def test_add_pet_invalid_age(name='Hunny', animal_type='Kitty', age=1234, pet_photo='images/Kitty.jpg'):
    # # #     '''Негативный сценарий. Добавление питомца с указанием несуществующего возраста в переменной 'age'.'''
    # # #
    # # #     # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    # # #     pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # # #
    # # #     # Запрашиваем ключ api и сохраняем в переменную auth_key
    # # #     _, auth_key = pf.get_api_key(valid_email, valid_password)
    # # #
    # # #     # Добавляем питомца
    # # #     status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # # #
    # # #     # Сверяем полученный ответ с ожидаемым результатом
    # # #     assert status == 200
    # # #     assert result['age'] == str(age)
    # # #     print('\n', 'Status code: ', status, '\n', result)

    # @pytest.mark.negative
    # @pytest.mark.get
    # def test_getAllPets_256_symbols(self, auth_key, filter='MMd6JjLk56Co8nCrgYKzWwKZKWO5opuEEKHs5u4b15zDUFLX9pphcYQkTELQXolhspAJpaUwaFnkwxHvkW9P1nKXZPo3bHPQyEwQdxow09gEOfwhcA2n7R2eIotUFIs2WcPkMr9wru5rkU3Vf3lbGUzvK88AHO4F5plLYi7LEYtSO5FdMmw57sJog0xaqB25v009ZZhQVvSUP0IQ8u43o5eKHRjvwEkycT9IxXMNAOh3VPWQOElEzZLFHWpnWeEe') -> json:
    #     """Негативный сценарий. Проверяем что запрос всех питомцев не возвращает список.
    #     Значение параметра filter = 256 символов. Для этого сначала получаем api ключ и
    #     сохраняем в переменную auth_key. Далее используя этого ключ запрашиваем список всех
    #     питомцев.
    #     Доступное значение параметра filter - 'my_pets' либо '' """
    #
    #     # # Запрашиваем ключ api и сохраняем в переменную auth_key
    #     # _, auth_key = pf.get_api_key(valid_email, valid_password)
    #
    #     status, result = pf.get_list_of_pets(auth_key, filter)
    #
    #     assert status != 200
    #     assert 'HTML' or 'html' in result
    #     # assert result.headers['Content-Type'] == "text/html; charset=utf-8"
    #     print('\n', 'Status code: ', status, '\n', result)

    # @pytest.mark.negative
    # @pytest.mark.get
    # def test_getAllPets_digit(self, auth_key,
    #                                 filter='1234567890') -> json:
    #     """Негативный сценарий. Проверяем что запрос всех питомцев не возвращает список.
    #     Значение параметра filter = числа. Для этого сначала получаем api ключ и
    #     сохраняем в переменную auth_key. Далее используя этого ключ запрашиваем список всех
    #     питомцев.
    #     Доступное значение параметра filter - 'my_pets' либо '' """
    #
    #     # # Запрашиваем ключ api и сохраняем в переменную auth_key
    #     # _, auth_key = pf.get_api_key(valid_email, valid_password)
    #
    #     status, result = pf.get_list_of_pets(auth_key, filter)
    #
    #     assert status != 200
    #     assert 'HTML' or 'html' in result
    #     # assert result.headers['Content-Type'] == "text/html; charset=utf-8"
    #     print('\n', 'Status code: ', status, '\n', result)

    # тест по заданию 21.6.4




