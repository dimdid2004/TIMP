# Импортируем необходимые библиотеки
import os

# Название файла, в котором будут храниться ФИО
filename = '/usr/local/share/fullnameDB/user_names.txt'

# Функция для сохранения ФИО
def save_name(name):
    with open(filename, 'a') as file:
        file.write(name + '\n')  

# Функция для проверки наличия ФИО в файле
def name_exists(name):
    if os.path.exists(filename):              # Проверяем, существует ли файл
        with open(filename, 'r') as file:
            names = file.read().splitlines()  # Читаем все строки из файла, разделяя по переносам строки
            return name in names              # Проверяем, есть ли ФИО в полученном списке
    return False                              


def main():
    # Запрашиваем у пользователя ФИО
    fio = input("[+] Введите ваше ФИО: ")
    
    # Проверяем наличие ФИО в файле
    if name_exists(fio):
        print("[-] Это ФИО уже существует в базе данных.")  
    else:
        save_name(fio) 
        print("[+] ФИО успешно сохранено.") 

# Запускаем главную функцию
if __name__ == "__main__":
    print(" --- Приветсвуем Вас в программе (time-limited) ---")
    main()