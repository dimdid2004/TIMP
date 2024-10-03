#!/bin/bash

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

