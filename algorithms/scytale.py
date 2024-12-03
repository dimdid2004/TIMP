import random
from cryptography.fernet import Fernet
KEY =  Fernet.generate_key()

class ScytaleError(Exception):
    pass


def encrypt_scytale(message: str) -> str:
    global KEY
 
    if not message:
        raise ScytaleError("Сообщение не должно быть пустым")
    if len(message) < 2:
        raise ScytaleError("Длина сообщения должна быть не менее 1 символов")

    m = get_random_key(message)
    print(f"Key: {m}")

    k = len(message) 

    n = (k - 1) // m + 1  # Количество столбцов

    encrypted_message_list = [""] * (n * m)
    for i in range(len(message)):
        # Вычисляем новый индекс
        index = m * (i % n) + i // n
        encrypted_message_list[index] = message[i]
    print(encrypted_message_list)
    encrypted_message = "".join(encrypted_message_list)
    encrypted_key = encrypt_message(str(m), KEY)
    return encrypted_message, encrypted_key


def decrypt_scytale(encrypted_message: str, key: str) -> str:
    """
    Расшифровывает сообщение, зашифрованное шифром Scytale.

    """
    if not encrypted_message:
        raise ScytaleError("Зашифрованное сообщение не должно быть пустым")
    
    
     # Расшифровываем ключ для Scytale
    m = int(decrypt_message(key, KEY))

    if not isinstance(m, int) or m <= 0:
        raise ScytaleError("Ключ должен быть положительным целым числом")

    k = len(encrypted_message)  # Длина зашифрованного сообщения
    if k % m not in [0, m-1]:
        raise ScytaleError("Неподходящий ключ для заданной длины сообщения")

    n = (k - 1) // m + 1  # Количество столбцов

    decrypted_message_list = [""] * (n * m)
    for i in range(len(encrypted_message)):
        # Вычисляем исходный индекс символа по обратной формуле
        index = n * (i % m) + i // m
        decrypted_message_list[index] = encrypted_message[i]
    return "".join(decrypted_message_list)

def get_possible_keys(message: str):
    keys = []
    len_msg = len(message)
    for i in range (1, len_msg):
        if len_msg % i in [0, i-1]:
            keys.append(i)
    return keys

def get_random_key(message: str):
    possible_keys = get_possible_keys(message)
    print(f"Possible keys: {possible_keys}")
    if possible_keys:
        return random.choice(possible_keys)
    else:
        return None  # Если нет возможных ключей



def generate_key():
    """
    Генерация ключа для симметричного шифрования (Fernet).
    """
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> str:
    """
    Шифрует сообщение с использованием симметричного шифрования.

    """
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message: str, key: bytes) -> str:
    """
    Расшифровывает зашифрованное сообщение с использованием симметричного шифрования.

    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

# Пример использования
# try:
#     original_message = "ТЕКСТПОСЛЕШИФРОВАНИЯСТАНЕТНЕПОНЯТНЫМ"

#     print(f"Возможные ключи для данного сообщения: {get_possible_keys(original_message)}")
#     # Шифрование
#     encrypted_message, key = encrypt_scytale(original_message)
#     print("Зашифрованное сообщение:", encrypted_message)
#     print("Ключ: ", key)

#     user_key = input("Введите ключ: ")
#     # Дешифрование
#     decrypted_message = decrypt_scytale(encrypted_message, user_key)
#     print("Расшифрованное сообщение:", decrypted_message)

# except ScytaleError as e:
#     print(f"Ошибка: {e}")
# except Exception as e:
#     print(f"Неожиданная ошибка: {e}")



