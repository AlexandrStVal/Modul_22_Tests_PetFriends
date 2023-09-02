'''Moduls 19, 20'''
import requests  # библиотека запросов
import json


# from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """api библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', timeout=2, headers=headers)
        # Как только клиент подключится к серверу и отправит HTTP-запрос, тайм-аут чтения - это количество секунд,
        # в течение которых клиент будет ждать ответа от сервера. (В частности, это количество секунд,
        # которое клиент будет ждать между байтами, отправленными с сервера

        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:  # если ошибка с форматом json
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
            со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
            либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
            собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', timeout=10, headers=headers, params=filter)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: int, pet_photo) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        #     data = MultipartEncoder(
        #         fields={
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')}
        res = requests.post(self.base_url + 'api/pets', timeout=10, headers=headers, data=data, files=file)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, timeout=2, headers=headers)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, timeout=2, headers=headers, data=data)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        # except json.decoder.JSONDecodeError:
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                                  age: int) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        #     data = MultipartEncoder(
        #         fields={
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/create_pet_simple', timeout=2, headers=headers, data=data)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_photo):
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'images/jpeg')}
        pet_id = '07293f4a-af31-43c1-b5d0-0268b28080d4'  # необходимо указать id животного для размещения фото
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, timeout=10, headers=headers, files=file)
        status = res.status_code
        # result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    # данные по заданию 21.6.4
    def api_request(self, session, method, url,
                    headers_update='',
                    data='',
                    json=''):

        if headers_update:
            session.headers.update(headers_update)
        if method in ['GET', 'POST', 'PUT', 'DELETE']:
            response = session.request(method, url, data=data, json=json)
        else:
            response = ''
        return response

