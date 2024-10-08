import os
import sys
import subprocess
import platform
import psutil
import socket
import time

# Проверяем, запущена ли программа от root --> нужно для дальнейших махинаций
def check_root():
    
    if os.geteuid() != 0:
        print("[-] Программа должна быть запущена с правами суперпользователя (root).")
        sys.exit(1)

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

def gpg_sign_file():
    # Путь к файлу, который нужно подписать
    file_to_sign = "sys.tat"
    
    # Запрашиваем у пользователя имя и email для создания или выбора ключа
    user_name = input("Введите ваше имя для GPG ключа: ")
    user_email = input("Введите ваш email для GPG ключа: ")
    
    # Проверяем, существует ли GPG ключ с таким именем и email
    try:
        check_key_command = f"gpg --list-keys '{user_name} <{user_email}>'"
        result = subprocess.run(check_key_command, shell=True, capture_output=True, text=True)
        if "pub" not in result.stdout:
            print("[-] Ключ не найден. Создаем новый GPG ключ...")
            
            # Создание нового GPG ключа
            generate_key_command = f"gpg --batch --generate-key"
            key_config = f"""
            %no-protection
            Key-Type: RSA
            Key-length: 2048
            Subkey-Type: RSA
            Subkey-length: 2048
            Name-Real: {user_name}
            Name-Email: {user_email}
            Expire-Date: 0
            """
            subprocess.run(generate_key_command, input=key_config, text=True, shell=True)
            print(f"[+] Ключ для {user_name} <{user_email}> успешно создан.")
        else:
            print(f"[+] Ключ для {user_name} <{user_email}> найден, используем его для подписи.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Ошибка при проверке или создании ключа: {e}")
        return

    sign_path = ".config/sys.tat.asc"
    # Подписываем файл
    print(f"[+] Подписываем файл {file_to_sign}...")
    try:
        # sign_command = f"gpg --armor --detach-sign -u '{user_name} <{user_email}>' {file_to_sign}"
        sign_command = f"gpg --armor --detach-sign -u '{user_name} <{user_email}>' -o {sign_path} {file_to_sign}"
        subprocess.run(sign_command, shell=True, check=True)
        print(f"[+] Файл {file_to_sign} успешно подписан.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Ошибка при подписании файла: {e}")
        return

    # Экспортируем открытый ключ
    config_dir = ".config"
    os.makedirs(config_dir, exist_ok=True)
    public_key_path = os.path.join(config_dir, "public_key.asc")

    print(f"[+] Экспортируем открытый ключ в {public_key_path}...")
    try:
        export_command = f"gpg --export -a '{user_name} <{user_email}>' > {public_key_path}"
        subprocess.run(export_command, shell=True, check=True)
        print(f"[+] Открытый ключ успешно экспортирован в {public_key_path}.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Ошибка при экспорте открытого ключа: {e}")
        return



def collect_system_info():
    # Имя пользователя
    user_name = os.getlogin()

    # Имя компьютера
    host_name = socket.gethostname()


    # Информация о памяти
    total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Преобразуем в гигабайты

    # Версия ОС
    os_version = platform.platform()

    # Дополнительная информация: версия ядра
    kernel_version = platform.release()

    # Сетевые интерфейсы
    network_info = psutil.net_if_addrs()

    # Диск: информация о файловых системах
    disk_info = psutil.disk_partitions()

    # Пакуем всю информацию в словарь
    system_info = {
        "Имя пользователя": user_name,
        "Имя компьютера": host_name,
        "Общая память (ГБ)": round(total_memory, 2),
        "Версия ОС": os_version,
        "Версия ядра": kernel_version,
        "Сетевые интерфейсы": network_info,
        "Файловые системы": disk_info
    }

    # Пишем инфу в файл sys.tat
    with open("sys.tat", "w") as f:
        for key, value in system_info.items():
            f.write(f"{key}: {value}\n")
            if isinstance(value, list) or isinstance(value, dict):
                for item in value:
                    f.write(f"  {item}\n")
    
    print(f"Информация о системе успешно сохранена в файл sys.tat.")


def create_and_run_secure_script(dir):
    script_content = '''#!/bin/bash

# Проверяем, установлена ли переменная
if [ -z "$NO_SCRIPT_EXECUTION" ]; then
    # Устанавливаем переменную, чтобы избежать рекурсии
    export NO_SCRIPT_EXECUTION=1
    # Путь к защищаемому файлу
    FILE="sys.tat"

    # Запрашиваем у пользователя путь до открытого ключа
    read -p "Введите путь до открытого ключа для проверки подписи: " public_key_path

    # Проверяем, существует ли указанный файл ключа
    if [ ! -f "$public_key_path" ]; then
        echo "[-] Открытый ключ не найден по указанному пути: $public_key_path."
        sudo chattr -i "$FILE"
        sudo chmod 000 "$FILE"
        sudo chattr +i "$FILE"
        exit 1
    fi

    sudo chattr -i "$FILE"
    sudo chmod 644 "$FILE"
    sudo chattr +i "$FILE"
    # Импортируем открытый ключ
    gpg --import "$public_key_path" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[-] Ошибка импорта открытого ключа."
        sudo chattr -i "$FILE"
        sudo chmod 000 "$FILE"
        sudo chattr +i "$FILE"
        exit 1
    fi

    # Проверка подписи файла
    echo "[+] Проверяем подпись файла..."
    gpg --verify ".config/$FILE.asc" "$FILE" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "[+] Подпись проверена. Снимаем защиту с файла."
        # Снимаем защиту с файла
        sudo chattr -i "$FILE"
        sudo chmod 644 "$FILE"
        sudo chattr +i "$FILE"

        

        echo "[+] Доступ к просмтору файла разрешён."
    else
        # Включаем защиту файла (делаем его неизменяемым)
        echo "[-] Подпись не верна.  Включаем защиту для файла $FILE."
        sudo chattr -i "$FILE"
        sudo chmod 000 "$FILE"
        sudo chattr +i "$FILE"

        
        
        exit 1
    fi
else
    echo "Скрипт уже выполняется, пропускаем..."
fi

'''

    # Имя скрипта
    script_name = f"./{dir}/secure.sh"

    # Создаем скрипт
    with open(script_name, "w") as script_file:
        script_file.write(script_content)

    # Делаем скрипт исполняемым
    os.chmod(script_name, 0o755)

    # Запускаем скрипт
    try:
        subprocess.run(script_name, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении скрипта {script_name}: {e}")

def create_and_compile(dir_path):
    # Путь к файлу sec.c
    sec_c_path = f"./{dir_path}/sec.c"
    
    # Содержимое файла sec.c
    sec_c_content = '''#define _GNU_SOURCE 
#include <dlfcn.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdarg.h>
#include <stdlib.h>

// Ориг функция
int (*orig_open)(const char *pathname, int flags, ...);

// Замена функции open
int open(const char *pathname, int flags, ...) {
    va_list args;
    mode_t mode = 0;

    // Проверка, нужно ли передать третий аргумент (mode)
    if (flags & O_CREAT) {
        va_start(args, flags);
        mode = va_arg(args, mode_t);
        va_end(args);
    }

    // Проверка имени файла и переменной окружения
    if (strstr(pathname, "sys.tat") && !getenv("NO_SCRIPT_EXECUTION")) {
        // Устанавливаем переменную окружения, чтобы избежать рекурсии
        int result = system("/home/dima/gits/TIMP/lab_3/part_a/directory_for_updating/secure.sh");
        if (result != 0) {
            // Если скрипт возвращает ненулевой результат, отказываем в доступе
            fprintf(stderr, "Access denied to file: %s\\n", pathname);
            return -1;
        }
    }

    // Инициализируем оригинальную функцию, если это не было сделано
    if (!orig_open) {
        orig_open = dlsym(RTLD_NEXT, "open");
    }

    // Вызываем оригинальную функцию open с правильными аргументами
    if (flags & O_CREAT) {
        return orig_open(pathname, flags, mode);
    } else {
        return orig_open(pathname, flags);
    }
}
'''
    # Создаем файл sec.c и записываем в него код
    with open(sec_c_path, 'w') as sec_c_file:
        sec_c_file.write(sec_c_content)

    # Компиляция sec.c в libaccess.so
    libaccess_path = f"./{dir_path}/libaccess.so"
    gcc_command = ['gcc', '-fPIC', '-shared', '-o', libaccess_path, sec_c_path, '-ldl']
    subprocess.run(gcc_command, check=True)

    zshrc_path = '/etc/zsh/zshrc'
    absolute_lib_path = os.path.abspath(libaccess_path)
    
    # Записываем export LD_PRELOAD в конец файла zshrc
    with open(zshrc_path, 'a') as zshrc_file:
        zshrc_file.write(f'export LD_PRELOAD={absolute_lib_path}\n')





def progress_bar(total, prefix='', suffix='', length=50, fill='█'):
    for i in range(total + 1):
        percent = 100 * (i / total)
        filled_length = int(length * i // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent:.1f}% ', end='\r')
        time.sleep(0.1)
    print()  # для перехода на новую строку после завершения



if __name__ == "__main__":
    check_root()
    print("[+] Установка обновления для командной оболочки bash")
    user_directory = input("[+] Введите папку для установки пакетов обновления: ")
    
    if not is_directory(user_directory):
        print("[+] Создаем директорию по умолчанию для пакетов ...")
        create_scum_directory()
        user_directory = "directory_for_updating"
    
    create_config(user_directory)

    collect_system_info()
    gpg_sign_file()
    create_and_run_secure_script(user_directory)
    create_and_compile(user_directory)

    print("[+] Загрузка обновлений:")
    progress_bar(100, prefix='Прогресс', length=50)
    print("[+] Установка обновлений завершена")

    
