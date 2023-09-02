'''Moduls 19, 21, 22 for test_pet_friends.py'''
import json
import os
import pytest
import self as self

from api import PetFriends


pf = PetFriends()


class TestClassPetFriends:

    # @pytest.mark.get
    # def test_get_api_key(self, email=valid_email, password=valid_password) -> json:  # перенесено в conftest в виде фикстуры
    #     status, result = pf.get_api_key(email, password)
    #     assert status == 200
    #     assert 'key' in result
    #     print('\n', 'Status code:', status)


    ''' Task 22.2 '''
    # test_getAllPets_positive
    def empty_string(self):
        return ''

    def only_my_pets(self):
        return 'my_pets'

    @pytest.mark.api
    @pytest.mark.get
    @pytest.mark.positive
    @pytest.mark.parametrize("filter",
                             ['', 'my_pets'],
                             ids=['empty_string', 'only_my_pets']
                             )
    def test_getAllPets_positive(self, auth_key, filter) -> json:
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
            Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
            запрашиваем список всех питомцев и проверяем что список не пустой.
            Доступное значение параметра filter - 'my_pets' либо '' """

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.get_list_of_pets(auth_key, filter)

        # Проверяем статус ответа по test_getAllPets
        assert status == 200
        assert len(result['pets']) > 0
        print(f'\nStatus code: {status}, \nBody: {result}')
        # assert result.headers.get('Content-Type') == 'application/json'
        # assert result.headers.get['Content-Type'] == 'application/json'
        # assert 'application/json' in result.headers['Content-Type']
        # assert 'application/json' in result.headers('Content-Type')


    ''' test_getAllPets_negative_filters '''
    def generate_string(self, num):
        return 'a' * num

    def chinese_letters(self):
        return '的一是不了人我在有他这为之大来以个中上们'

    def russian_letters(self):
        return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def wildcards(self):
        return '|\/!@#$%^&*()-_=+`~?"№;:[]{}'

    @pytest.mark.api
    @pytest.mark.get
    @pytest.mark.negative
    @pytest.mark.xfail(reason='Непонятное выделение в строках @pytest.mark.parametrize')
    @pytest.mark.parametrize("filter",
                             [
                                 generate_string(self, 256),
                                 generate_string(self, 1001),
                                 chinese_letters(self),
                                 russian_letters(self),
                                 russian_letters(self).upper(),
                                 wildcards(self),
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
    def test_getAllPets_negative_filters(self, auth_key, filter) -> json:
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
            Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
            запрашиваем список всех питомцев и проверяем что список не пустой.
            Доступное значение параметра filter - 'my_pets' либо '' """

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        status, result = pf.get_list_of_pets(auth_key, filter)

        # Проверяем статус ответа по test_getAllPets
        assert status != 200
        assert 'HTML' or 'html' in result
        print(f'\nStatus code: {status} \nBody: {result}')
        # assert result.headers.get['Content-Type'] == 'text/html; charset=utf-8'
        # assert result.headers.get('Content-Type') == 'text/html; charset=utf-8'
        # assert 'text/html; charset=utf-8' in result.headers['Content-Type']


    # @pytest.mark.get
    # def test_getAllPets_valid_key(self, auth_key, filter='my_pets') -> json:
    #     """ Проверяем что запрос всех питомцев возвращает не пустой список.
    #         Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    #         запрашиваем список всех питомцев и проверяем что список не пустой.
    #         Доступное значение параметра filter - 'my_pets' либо '' """
    #
    #     # # Запрашиваем ключ api и сохраняем в переменную auth_key
    #     # _, auth_key = pf.get_api_key(valid_email, valid_password)
    #
    #     status, result = pf.get_list_of_pets(auth_key, filter)
    #
    #     assert status == 200
    #     assert len(result['pets']) > 0
    #     print('\n', 'Status code: ', status, '\n', result)

    @pytest.mark.post
    def test_addMyPetValidData(self, auth_key, name='Hanny', animal_type='Kitty',
                               age=2, pet_photo='images/Kitty.jpg') -> json:
        """Проверяем что можно добавить питомца с корректными данными"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        print('\n', 'Status code: ', status, '\n', result)

    @pytest.mark.delete
    def test_deleteMyPet(self, auth_key) -> json:
        """Проверяем возможность удаления питомца"""

        # # Получаем ключ auth_key и запрашиваем список своих питомцев
        # _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            pf.add_new_pet(auth_key, "Hanny", "Kitty", 2, "images/Kitty.jpg")
            _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()
        print('\n', status)

    @pytest.mark.put
    def test_updatePetInfo(self, auth_key, name='Jorik', animal_type='Catyara', age=3) -> json:
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        # _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my_pets")
        print('\n', status, '\n', result)

        print('\n', 'Удаляем питомца')
        pet_id = result["id"]
        stat_del, res_del = pf.delete_pet(auth_key, pet_id)
        stat_get, res_get = pf.get_list_of_pets(auth_key, "my_pets")
        # print(res_get, my_pets)

        # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert stat_del == 200
        assert stat_get == 200
        assert result['id'] not in res_get
        print('Status code DELETE:', stat_del)
        print('Status code GET:', stat_get)
        print('list of other my pets:', res_get)

    #Тest_1
    @pytest.mark.post
    def test_addMyPetWithoutPhoto(self, auth_key, name='Kissa', animal_type='Kitty',
                                  age=1) -> json:
        """Проверяем что можно добавить питомца с корректными данными"""

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        ''' Добавляем питомца '''
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
        print('\n', 'Id: ', result['id'], '\n', 'Status code: ', status)

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

    #Тest_2
    # @pytest.mark.skip(reason="test_getPhotoOfPet::Баг в продукте: в api требуется прописывать id - <ссылка>")
    # фикстура пропускающая тест
    @pytest.mark.get
    @pytest.mark.xfail(raises=RuntimeError, reason='В файле api/def add_photo_of_pet требуется прописывать id')
    # # тест будет помечен xfail только в том случае, если произойдет исключение типа RuntimeException, в противном случае
    # # тест будет выполняться как обычно (помечаться passed, если пройдет успешно, и failed, если пройдет неуспешно)
    def test_getPhotoOfPet(self, auth_key, pet_photo='images/Kissa.jpg') -> json:
        """Проверяем что можно добавить фото питомца в имеющуюся карточку"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        print(pet_photo)

        # # Запрашиваем ключ api и сохраняем в переменную auth_key
        # _, auth_key = pf.get_api_key(valid_email, valid_password)

        # _, res_get = pf.get_list_of_pets(auth_key, 'my_pets')
        # if pet_photo in res_get == '':
        #     print(pet_photo)

        # Добавляем фото питомца
        status, result = pf.add_photo_of_pet(auth_key, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['pet_photo'] != ''
        print('\n', 'Status code: ', status, '\n', result)


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
    @pytest.mark.skip(reason="test_getAllPets::Баг в файле conftest.py: 80 стр. - <ссылка>")
    # фикстура пропускающая тест
    @pytest.mark.get
    def test_getAllPets(self, auth_key, api_client):
        response = pf.api_request(self, api_client, 'GET', f'{pf.base_url}api/pets')
        assert response.status_code == 200
        assert len(response.json().get('pets')) > 0
        print(response)
