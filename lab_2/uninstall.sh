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

# Удаление папки с данными пользователей
FIO_DIR="/usr/local/share/fullnameDB/"
if [ -d "$FIO_DIR" ]; then
    echo "Удаление файла c пользовательскими данными..."
    rm -rf "$FIO_DIR"
    echo "Файл успешно удалён."
fi

echo "Деинсталяция завершена."
