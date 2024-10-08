#!/usr/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "[-] Деинсталяция должна производиться под root-пользователем"
    exit 1
fi


# Путь к исполняемому файлу
PROGRAM_PATH="sys_doc"

# Проверяем, установлен ли исполняемый файл
if [ -f "$PROGRAM_PATH" ]; then
    echo "[+] Удаление установщика обновлений ..."

    # Удаление исполняемого файла
    rm -f "$PROGRAM_PATH"
    
    echo "[+] Программа успешно удалена."
else
    echo "[-] Установщик обновлений не найден. Возможно, он не был установлен."
    exit 1
fi

# Путь к файлу
file="/etc/zsh/zshrc"

# Строка, которую нужно удалить
string_to_remove="export LD_PRELOAD=/home/dima/gits/TIMP/lab_3/part_a/libaccess.so"

# Удаление строки из файла
sed -i "\|$string_to_remove|d" "$file"

echo "[+] Удаляем директорию с данными обновления ..."

# Абсолютный путь к конфигурационному файлу в домашней директории пользователя
conf=".config/config.txt"

# Проверяем, существует ли конфигурационный файл
if [ -f "$conf" ]; then
    # Читаем user_dir из конфигурационного файла
    user_dir=$(grep "^user_dir=" "$conf" | cut -d'=' -f2)

    # Проверяем, существует ли директория, указанная в user_dir
    if [ -d "$user_dir" ]; then
        rm -rf "$user_dir"
        echo "[+] Директория успешно удалена"
    else
        echo "[-] Директория не найдена"
    fi
else
    echo "[-] Данные не найдены."
fi

echo "[+] Удаляем конфигурационные данные ..."
rm -rf ".config"
echo "[+] Данные успешно удалены"


# удаляем подпись
SYS_TAT_ASC="sys.tat.asc"
if [ -f "$SYS_TAT_ASC" ]; then
    # Удаление исполняемого файла
    rm -f "$SYS_TAT_ASC"    
fi

sudo chattr -i sys.tat   
# удаляем sys.tat
SYS_TAT="sys.tat"
if [ -f "$SYS_TAT" ]; then
    # Удаление исполняемого файла
    rm -f "$SYS_TAT"    
fi

gpg --yes --delete-secret-keys "dima <dima@did.ua>" 
gpg --yes --delete-key "dima <dima@did.ua>" 




echo "[+] Деинсталяция завершена."