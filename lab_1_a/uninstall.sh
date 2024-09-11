#!/usr/bin/bash

# Путь к исполняемому файлу
PROGRAM_PATH="$(pwd)/security_manager"

# Проверяем, установлен ли исполняемый файл
if [ -f "$PROGRAM_PATH" ]; then
    echo "[+] Удаление программы security_manager ..."

    # Удаление исполняемого файла
    rm -f "$PROGRAM_PATH"
    
    echo "[+] Программа успешно удалена."
else
    echo "[-] Программа 'security_manager ' не найдена. Возможно, она не была установлена."
    exit 1
fi

# Удаление файла с данными пользователей
FIO_FILE="$(pwd)/template.tbl"
if [ -f "$FIO_FILE" ]; then
    echo "[+] Удаление файла c пользовательскими данными..."
    rm -f "$FIO_FILE"
    echo "[+] Файл успешно удалён."
fi

echo "[+] Деинсталяция завершена."
