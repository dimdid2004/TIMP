import os
import time
import threading

# Название файла, в котором будут храниться ФИО
filename = '/usr/local/share/fullnameDB/user_names.txt'

# Путь до файла с информацией о времени работы программы:
file_start_restrict = '/usr/local/share/fullnameDB/.time_restrict.txt'
TIME_LIMIT = 30 

#переменная-сигнал для завершения ф-ии, производящей мониторинг
not_end = 1

lock = threading.Lock()

def check_time_limit():
    global file_start_restrict
    if os.path.exists(file_start_restrict):
        with open(file_start_restrict, 'r') as file:
            total_time = int(file.read())
    else:
        total_time = 0
    
    return total_time

def monitor_time(total_time):
    start_time = time.time()
    global file_start_restrict, not_end
    while not_end:
        current_time = time.time()
        used_time = int(current_time - start_time)
        
        if total_time + used_time > TIME_LIMIT:
            print("\n[-] Вы превысили лимит времени использования программы.")
            print("    Пожалуйста, приобретите полную версию или удалите программу.")
            
            # Сохраняем накопленное время в файл перед завершением
            with open(file_start_restrict, 'w') as file:
                file.write(str(TIME_LIMIT))  # записываем лимит, чтобы при следующем запуске программа знала, что лимит исчерпан

            os._exit(0)  # Завершаем программу
        else:
            # Обновляем накопленное время использования
            with open(file_start_restrict, 'w') as file:
                file.write(str(total_time + used_time))
        
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
    fio = input("[+] Введите ваше ФИО: ")
    
    # Проверяем наличие ФИО в файле
    if name_exists(fio):
        print("[-] Это ФИО уже существует в базе данных.")  
    else:
        save_name(fio) 
        print("[+] ФИО успешно сохранено.") 
    global lock, not_end
    with lock:
        not_end = 0

if __name__ == "__main__":
    print(" --- Приветсвуем Вас в программе fullnameDB (time-limited) ---")
    total_time = check_time_limit()
    if total_time >= TIME_LIMIT:
        print("[-] Вы уже превысили лимит времени использования программы")
        print("    Пожалуйста, приобретите полную версию или удалите программу.")
        os._exit(0)
    print(f"[INFO] Оставшееся время пользования пробной версией: {TIME_LIMIT - total_time} секунд")
    
    # Мониторингом времени использования будет заниматься отдельный поток
    time_monitoring = threading.Thread(target=monitor_time, args=(total_time,))
    time_monitoring.start()

    main()

    time_monitoring.join()