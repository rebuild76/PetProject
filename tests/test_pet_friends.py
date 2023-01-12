from api import PetFriends
from settings import creds
import os

pf = PetFriends()


# 1. Тест на получение токена
def test_get_api_key_for_valid_user(email=creds['valid_email'], password=creds['pass']):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


# 2. Тест получения списка животных
def test_get_all_pets_with_valid_data():
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert len(result['pets']) > 0


# 3. Тест на создание питомца без фото
def test_create_pet_without_photo():
    age = "10"
    name = "Gidropon"
    type = "snake"
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, type, age)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type


# 4. Позитивный тест с созданием питомца с вызовом api на загрузку фото
def test_add_pet_photo():
    age = "1"
    name = "Сурик"
    animal_type = "кот"
    pet_photo = "images/111.jpeg"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, animal_type, age)
    new_status, new_result = pf.set_pet_photo(auth_key, result["id"], pet_photo)
    assert new_status == 200


# 5. Тест на проверку создание питомца с фото
def test_create_pet_with_photo():
    age = "3"
    name = "Alon"
    type = "Creep"
    pet_photo = "images/111.jpeg"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
    assert result['name'] == name
    assert result['animal_type'] == type
    assert "data:image/jpeg;base64" in result['pet_photo']


# 6. Проверка обновления
def test_sucsessful_update_pet_info():
    age = "2"
    name = "Фуфырик"
    animal_type = "шуршунчик"
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.change_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Не доступных питомцев')


# 7. Проверка удаления
def test_sucessful_delete_pet():
    age = "1"
    name = "Puzik"
    type = "cat"
    pet_photo = "images/111.jpeg"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, pet_photo)
    status_delete, result_delete = pf.delete_pet(auth_key, result["id"])
    assert status_delete == 200


# 8. Негативный тест с не валидной почтой
def test_get_api_key_for_invalid_user(email=creds['invalid_email'], password=creds['pass']):
    status, result = pf.get_api_key(email, password)
    assert status == 403


# 9. Негативный тест создания без фото и без "animal_type"
def test_create_pet_without_photo_without_animal_type_field():
    age = '5'
    name = "Grundik"
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_simple_without_photo_without_animal_type_field(auth_key, name, age)
    assert status == 400


# 10. Негативный тест с некорректным auth-key
def test_create_pet_without_photo_with_invalid_auth_key():
    age = "4"
    name = "Lolik"
    animal_type = "Слон"
    status, result = pf.add_new_pet_simple_without_photo(auth_key={'key': 'incorrect_key'},
                                                name=name, animal_type=animal_type, age=age)
    assert status == 403


# 11. Негативный тест с файлом рандомным вместо фото
def test_create_pet_with_invalid_photo():
    age = "1"
    name = "Пес"
    type = "pop"
    pet_photo = "images/radm.pp"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_with_photo(auth_key, name, type, age, pet_photo)
    assert status == 400


# 12. Проверка создания с некорректным auth_key
def test_create_pet_with_photo_with_invalid_auth_key():
    age = "1"
    name = "LLLo"
    type = "nitka"
    pet_photo = "images/111.jpeg"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_with_photo(auth_key={'key': 'incorrect_key'},
                                               name=name, animal_type=type,
                                               age=age, pet_photo=pet_photo)
    assert status == 403


# 13. проверяем можно ли добавить фото питомца с некорректным auth-key
def test_add_pet_photo_invalid_auth_key():
    age = "3"
    name = "Yan"
    type = "snake"
    pet_photo = "images/pes1.jpg"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(creds['valid_email'], creds['pass'])
    status, result = pf.add_new_pet_simple_without_photo(auth_key, name, type, age)
    status, result = pf.set_pet_photo(auth_key={'key': 'incorrect_key'}, pet_id=result["id"], pet_photo=pet_photo)
    assert status == 403