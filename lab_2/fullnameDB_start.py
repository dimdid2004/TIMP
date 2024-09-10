# Импортируем необходимые библиотеки
import os

# Название файла, в котором будут храниться ФИО
filename = '/usr/local/share/fullnameDB/user_names.txt'

# Путь до файла с информацией о кол-ве запусков:
file_start_restrict = '/usr/local/share/fullnameDB/.start_restrict.txt'
START_LIMIT = 3

# Ф-ия для проверки лимитов использования
def check_start_limit():
    global file_start_restrict
    if os.path.exists(file_start_restrict):
        with open(file_start_restrict, 'r') as file:
            count = int(file.read())
    else:
        count = 0
    
    with open(file_start_restrict, 'w') as file:
            count += 1
            file.write(str(count))

    return count
    # if count >= START_LIMIT:
    #     print("Вы превысили лимит запусков программы.")
    #     print("Пожалуйста, приобретите полную версию или удалите программу.")
    #     return False
    # else:
    #     with open(file_start_restrict, 'w') as file:
    #         file.write(str(count + 1))
    #     return True

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
    print(" --- Приветсвуем Вас в программе fullnameDB (start-limited) ---")
    num_of_starts = check_start_limit()
    if num_of_starts > START_LIMIT:
        print("[-] Вы превысили лимит запусков программы.")
        print("    Пожалуйста, приобретите полную версию или удалите программу.")
        os._exit(0)
    print(f"[INFO] Осталось запусков: {START_LIMIT-num_of_starts}")

    main()