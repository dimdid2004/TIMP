#!/usr/bin/bash

# Путь к исполняемому файлу
PROGRAM_PATH="/usr/local/bin/fullnameDB"

# Проверяем, установлен ли исполняемый файл
if [ -f "$PROGRAM_PATH" ]; then
    echo "Удаление программы fullnameDB ..."

    # Удаление исполняемого файла
    rm -f "$PROGRAM_PATH"
    
    echo "Программа успешно удалена."
else
    echo "Программа 'fullnameDB' не найдена. Возможно, она не была установлена."
    exit 1
fi

# Удаление файла с данными пользователей
FIO_FILE="/usr/local/share/fullnameDB/user_names.txt"
if [ -f "$FIO_FILE" ]; then
    echo "Удаление файла c пользовательскими данными..."
    rm -f "$FIO_FILE"
    echo "Файл успешно удалён."
fi

echo "Деинсталяция завершена."
