import os.path

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_new_pet_added_with_valid_data(name = 'Гура', animal_type = 'Большая белая акула', age = '18',
                                       pet_photo ='images/shark.jpg' ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_pet_successfully_deleted():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Гура', 'Большая белая акула', '18', 'images/shark.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_pet_successfully_updated(name = 'Gura', animal_type = 'Большая белая акула', age = '20'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('No pets found')


def test_new_pet_simple_added_with_valid_data(name = 'Гура', animal_type = 'Большая белая акула', age = '18'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_pet_photo_successfully_updated(pet_photo = 'images/shark2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ''
        assert 'pet_photo' in result
    else:
        raise Exception('No pets found')

# Tests =======================

def test_get_api_key_invalid_email(email = 'invalidmail.com', password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_invalid_password(email = valid_email, password = 'invalidpassword'):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_empty_email(email = '', password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_empty_password(email = valid_email, password = ''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_all_pets_with_incorrect_filter(filter='my_animals'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    assert 'Filter value is incorrect' in result

def test_get_all_pets_with_ivalid_auth_key(filter=''):
    auth_key = {'key': 'dbsajdbasjkh3ahwajkh3aw3haw3h3awj3ha'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result

def test_new_pet_added_with_valid_data_wrong_auth_key(name = 'Гура', animal_type = 'Большая белая акула', age = '18',
                                       pet_photo ='images/shark.jpg' ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {'key': 'dbsajdbasjkh3ahwajkh3aw3haw3h3awj3ha'}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert 'Forbidden' in result

def test_new_pet_added_with_letters_in_age(name = 'Гура', animal_type = 'Большая белая акула', age = 'dasdas',
                                       pet_photo ='images/shark.jpg' ):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if status == 200:
        print('BUG: Параметр age пропускает буквенные значения')

    assert status == 403
    assert 'Forbidden' in result

def test_pet__delete_pet_ivalid_pet_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Гура', 'Большая белая акула', '18', 'images/shark.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = 'dsaddsadas'
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if not status == 403:
        print(f' BUG: При вводе неверного pet_id вместо кода 403 выдается {status}')

    assert status == 403

def test_pet_updated_with_invalid_pet_id(name = 'Gura', animal_type = 'Большая белая акула', age = '20'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'dsaddsadas'
    status, result = pf.update_pet(auth_key, pet_id, name, animal_type, age)

    assert status == 400
    assert 'Bad Request' in result

def test_new_pet_simple_added_with_invalid_auth_key(name = 'Гура', animal_type = 'Большая белая акула', age = '18'):
    auth_key = {'key': 'dbsajdbasjkh3ahwajkh3aw3haw3h3awj3ha'}
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 403
    assert 'Forbidden' in result

def test_pet_photo_updated_with_invalid_pet_id(pet_photo = 'images/shark2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'dsaddsadas'
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    if not status == 403:
        print(f' BUG: При вводе неверного pet_id вместо кода 403 выдается {status}')

    assert status == 403

    

