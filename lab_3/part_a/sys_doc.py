import os
import sys

# Проверяем, запущена ли программа от root --> нужно для дальнейших махинаций
def check_root():
    
    if os.geteuid() != 0:
        print("Программа должна быть запущена с правами суперпользователя (root).")
        sys.exit(1)
    else:
        print("Программа запущена с правами root, продолжаем выполнение.")

def is_directory(dir):
    return os.path.isdir(dir)

def create_scum_directory():
    scum_dir = "directory_for_updating"
    wd = os.getcwd()
    path = os.path.join(wd, scum_dir)
    try:
        os.mkdir(path)
        print("[+] Директория успешно создана")
    except Exception as ex:
        print(f"[-] Ошибка при создании директории: {ex}")

def create_config(user_dir_value):
    config_dir = ".config"
    config_file = os.path.join(config_dir, "config.txt")
    
    # Создаем директорию, если она не существует
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # Записываем значение user_dir в файл
    with open(config_file, "w") as f:
        f.write(f"user_dir={user_dir_value}\n")
    
    print(f"Конфигурационный файл создан: {config_file}")

if __name__ == "__main__":
    check_root()
    print("[+] Установка обновления для командной оболочки bash")
    user_directory = input("[+] Введите папку для установки пакетов обновления: ")
    
    if not is_directory(user_directory):
        print("[+] Создаем директорию по умолчанию для пакетов ...")
        create_scum_directory()
        user_directory = "directory_for_updating"
    
    create_config(user_directory)
