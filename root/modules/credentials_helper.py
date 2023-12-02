# ------- Logowanie/Rejestracja -------

# Zewnetrzne biblioteki
import random
import string
import hashlib
import binascii 

class UserPass:

 def __init__(self, user='', password=''):
    self.user = user
    self.password = password

 def hash_password(self):
    '''Hashuje haslo do przechowania'''
    # wartosc generowana za pomoca os.urandom(60) do tworzenia 'soli'
    os_urandom_static =b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
    # praktyka 'solenia' hasla
    # hash hasla wyliczany za pomoca algorytmu sha512
    salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)

    # Zdekodowana do postaci ascii postac zahashowanego hasla
    return (salt + pwdhash).decode('ascii') 

 def verify_password(self, stored_password, provided_password):
    '''Sprawdza poprawnosc hasla uzytkownika'''
    # stored_password to postac zahashowana razem z sola
    # wykonuje taki sam proces co metoda hash_password tylko z podanym haslem
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),
    salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

 def get_random_user_pasword(self):
    'wygeneruj losowego uzytkownika z losowym hashlem'
    random_user = ''.join(random.choice(string.ascii_lowercase)for i in range(3))
    self.user = random_user

    password_characters = string.ascii_letters #+ string.digits + string.punctuation
    random_password = ''.join(random.choice(password_characters)for i in range(3))
    self.password = random_password 
