#!/usr/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "[-] Инсталяция должна производиться под root-пользователем"
    exit 1
fi

echo " --- Формируем установщик обновлений bash ---"

VENV=".venv"
if [ ! -d "${VENV}" ]; then
    echo "Создаем виртуальное окружение с требуемыми зависимостями ..."
    python -m venv "$VENV"

    source "$VENV/bin/activate"

    pip install -r requirements.txt

    echo -e "\n\n"
fi

pyinstaller --onefile sys_doc.py --distpath "$(pwd)"
   
chmod +x sys_doc

# Удаляем ненужные временные файлы 
rm -rf build/ sys_doc.spec

echo "Установка успешно завершена."