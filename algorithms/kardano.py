import numpy as np
import random
from cryptography.fernet import Fernet
import math

KEY = Fernet.generate_key()

class GrilleError(Exception):
    pass

def calculate_k(text_length):
    """Автоматический подбор оптимальной по размеру решетки для текста"""
    # Находим минимальное k, при котором 4k² >= длине текста
    k = math.ceil(math.sqrt(text_length / 4))
    return k

def generate_code(k):
    """Генерирует случайный код для решетки"""
    code_length = k * k
    positions = ['1', '2', '3', '4']
    code = ''.join(random.choices(positions, k=code_length))
    return code

# Вспомогательные функции для шифрования/дешифрования ключа
def encrypt_message(message: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt_message(encrypted_message: str, key: bytes) -> str:
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()

def rotate_90(matrix):
    return np.rot90(matrix, -1)

def create_grille(k):
    base = np.arange(1, k*k + 1).reshape(k, k)
    result = np.empty((2, 2), dtype=object)
    result[0, 0] = base
    result[0, 1] = rotate_90(base)
    result[1, 1] = rotate_90(result[0, 1])
    result[1, 0] = rotate_90(result[1, 1])
    return result

def get_positions(k, code, rotation=0):
    positions = []
    grille = create_grille(k)
    
    for i, position in enumerate(code):
        if position == '1':
            quad_row, quad_col = 0, 0
        elif position == '2':
            quad_row, quad_col = 0, 1
        elif position == '3':
            quad_row, quad_col = 1, 1
        elif position == '4':
            quad_row, quad_col = 1, 0
            
        quad = grille[quad_row, quad_col]
        row, col = np.where(quad == i+1)
        
        abs_row = quad_row * k + row[0]
        abs_col = quad_col * k + col[0]
        
        for _ in range(rotation):
            old_row, old_col = abs_row, abs_col
            abs_row = old_col
            abs_col = 2*k - 1 - old_row
            
        positions.append((abs_row, abs_col))
    
    return positions

def encrypt_text(text, k, code):
    full_length = min(4 * k * k, len(code) * 4) 
    text = text[:full_length].ljust(full_length, '#')
    
    result = np.full((2*k, 2*k), '*', dtype=str)
    pos = 0
    rotation = 0
    
    while pos < len(text) and rotation < 4:
        positions = get_positions(k, code, rotation)
        
        for row, col in positions:
            if pos < len(text):
                result[row, col] = text[pos]
                pos += 1
            else:
                break
        rotation += 1
    print(result)
    # Формируем криптограмму
    cryptogram = ''.join(result.flatten())
    return cryptogram, result

def decrypt_text(cryptogram, k, code):
    # Восстанавливаем матрицу из криптограммы
    matrix = np.array(list(cryptogram)).reshape(2*k, 2*k)
    
    # Собираем все позиции для всех поворотов
    all_positions = []
    for rotation in range(4):
        positions = get_positions(k, code, rotation)
        all_positions.extend(positions)
    
    # Восстанавливаем исходный текст
    decrypted = [''] * len(all_positions)
    for i, (row, col) in enumerate(all_positions):
        decrypted[i] = matrix[row, col]
    
    # Убираем символы заполнения
    decrypted_text = ''.join(decrypted).rstrip('#')
    return decrypted_text



def encrypt_grille(text: str) -> tuple:
    """
    Шифрует сообщение с помощью поворотной решетки.

    """
    if not text:
        raise GrilleError("Сообщение не должно быть пустым")
    
    if len(text) < 4:
        raise GrilleError("Длина сообщения должна быть не менее 4 символов")
    # Определяем размер решетки
    k = calculate_k(len(text))
    
    # Генерируем случайный код
    code = generate_code(k)
    # code = "242431134"
    print(f"Code: {code}")
    # Шифруем текст
    cryptogram, matrix = encrypt_text(text, k, code)
    
    # Шифруем код
    encrypted_code = encrypt_message(f"{k}:{code}", KEY)
    
    return cryptogram, encrypted_code

def decrypt_grille(encrypted_message: str, encrypted_code: str) -> str:
    """
    Расшифровывает сообщение, зашифрованное поворотной решеткой.

    """
    if not encrypted_message or not encrypted_code:
        raise GrilleError("Зашифрованное сообщение и код не должны быть пустыми")

    # Расшифровываем код
    decrypted_code = decrypt_message(encrypted_code, KEY)
    k, code = decrypted_code.split(':')
    k = int(k)
    
    # Расшифровываем сообщение
    decrypted = decrypt_text(encrypted_message, k, code)
    
    return decrypted

# Пример использования
# try:
#     original_message = "ТЕКСТПОСЛЕШИФРОВАНИЯСТАНЕТНЕПОНЯТНЫМ"

#     # Шифрование
#     encrypted_message, encrypted_code = encrypt_grille(original_message)
#     print("Зашифрованное сообщение:", encrypted_message)
#     print("Зашифрованный код:", encrypted_code)

#     # Дешифрование
#     decrypted_message = decrypt_grille(encrypted_message, encrypted_code)
#     print("Расшифрованное сообщение:", decrypted_message)

# except GrilleError as e:
#     print(f"Ошибка: {e}")
# except Exception as e:
#     print(f"Неожиданная ошибка: {e}")
