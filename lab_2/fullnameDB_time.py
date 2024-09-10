# Импортируем необходимые библиотеки
import os

# Название файла, в котором будут храниться ФИО
filename = '/usr/local/share/fullnameDB/user_names.txt'

# Путь до файла с информацией о времени работы программы:
file_start_restrict = '/usr/local/share/fullnameDB/.time_restrict.txt'
TIME_LIMIT = 30 

def check_time_limit():
    if os.path.exists(time_file):
        with open(time_file, 'r') as file:
            start_time = int(file.read())
    else:
        start_time = time.time()
        with open(time_file, 'w') as file:
            file.write(str(start_time))
    
    return start_time

def monitor_time(start_time):
    while True:
        if time.time() - start_time > TIME_LIMIT:
            print("[-] Вы превысили лимит времени использования программы.")
            print("    Пожалуйста, приобретите полную версию или удалите программу.")
            os._exit(0)  # Завершаем программу
        time.sleep(1)  # Проверяем каждую секунду

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
    print(" --- Приветсвуем Вас в программе fullnameDB (time-limited) ---")
    main()