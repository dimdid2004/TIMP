#!/usr/bin/bash
# Запрос выбора версии программы
echo "Выберите версию программы для установки:"
echo "1. Time-limited"
echo "2. Start-limited"
read -p "Введите номер версии (1 или 2): " version

PROG_DIR="/usr/local/bin/"

# Проверка выбора и компиляция соответствующего скрипта
if [ "$version" -eq 1 ]; then
    program_name="fullnameDB_time"
    # Компилируем time-limited программу в .exe
    pyinstaller --onefile fullnameDB_time.py --distpath "${PROG_DIR}"
   
    echo "Установлена версия Time-limited."
elif [ "$version" -eq 2 ]; then
    program_name="fullnameDB_start"
    # Компилируем start-limited программу в .exe
    pyinstaller --onefile fullnameDB_start.py --distpath "${PROG_DIR}"
    echo "Установлена версия Start-limited."
else
    echo "Неверный номер версии. Установка отменена."
    exit 1
fi

 # Переименовываем исполняемый файл 
mv "/usr/local/bin/${program_name}" /usr/local/bin/fullnameDB

# Устанавливаем права на исполняемый файл
chmod +x "${PROG_DIR}/fullnameDB"

# Создаем директорию под файл с данными
if [ ! -d "/usr/local/share/fullnameDB/" ]; then
    mkdir /usr/local/share/fullnameDB/
fi
# Удаляем ненужные временные файлы 
rm -rf build/ fullnameDB_*.spec

echo "Установка успешно завершена."