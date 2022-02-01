from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверяем, что код статуса запроса 200 и в переменной result содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем, что код статуса запроса 200 и список всех питомцев не пустой.
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
    api_key, затем применяем метод get_list_of_pets(), проверяем статус ответа и то
    что список питомцев не пустой'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Basya', animal_type="cat", age='8', pet_photo='images/pexels-lina-kivaka-1741205.jpg'):
    '''Проверяем, что код статуса запроса 200 и что список с добавленными данными не пустой. Для этого
    в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
    проверяем статус ответа и что в ответе содержатся добавленные данные.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Supercat', 'cat2', '2', 'images/pexels-ihsan-adityawarman-1056251.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    '''Берём id первого питомца из списка и отправляем запрос на удаление'''
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    '''Ещё раз запрашиваем список своих питомцев'''
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    '''Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца'''
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_pet_info(name='Vasya', animal_type='cat3', age=1):
    '''Проверяем возможность изменения данных питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")
def test_successful_create_pet_simple_without_photo(name='Bob', animal_type='kitten', age=2):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_to_pet_that_exist(pet_photo='images/pexels-katarzyna-modrzejewska-1314550.jpg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pet")

def test_get_api_key_with_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_invalid_email_and_valid_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с валидным паролем и с невалидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_negative_age(name='Molly', animal_type='kitten', age='-2', pet_photo='images/pexels-ihsan-adityawarman-1056251.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert int(result['age']) < 0

def test_add_new_pet_with_invalid_age(name='Lucky', animal_type='puppy', age='120', pet_photo='images/pexels-denniz-futalan-2523934.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более 2 знаков в переменной age.
    Тест не будет пройден, ели питомец будет добавлен на сайт с числом превышающим 2 знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert int(result['age']) > 99


def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='2', pet_photo='images/pexels-ihsan-adityawarman-1056251.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "name"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert len(result['name']) == 0, 'Пожалуйста, укажите имя питомца'


def test_add_pet_with_empty_value_in_variable_animal_type(name='Max', animal_type='', age='20', pet_photo='images/pexels-ihsan-adityawarman-1056251.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной animal_type
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "animal_type"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert len(result['animal_type']) == 0, 'Пожалуйста, укажите породу питомца'


def test_add_pet_with_empty_value_in_variable_age(name='Mikki', animal_type='cat', age='', pet_photo='images/pexels-ihsan-adityawarman-1056251.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной age
    Тест не будет пройден, если питомец будет добавлен на сайт с пустым значением в поле "age"'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert len(result['age']) == 0, 'Пожалуйста, укажите возраст питомца'


def test_failed_add_new_pet_with_incorrect_file_format(name='Safari', animal_type='animals', age='5', pet_photo='images/Safari_Animals.eps'):
    '''Проверяем возможность добавления нового питомца c фото неподходящeго форматa .eps
     Тест не будет пройден, если питомец будет добавлен на сайт с фото неподходящeго форматa'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200

def test_add_new_pet_with_incorrect_data_type_in_variable_name(name=123, animal_type='dog', age='1', pet_photo='images/pexels-denniz-futalan-2523934.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной name.
    Тест не будет пройден, если питомец будет добавлен на сайт с цифрами вместо букв в поле name'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email,valid_password)
    _, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert name not in result['name'], 'Питомец добавлен на сайт с цифрами вместо букв в поле name'











