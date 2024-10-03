#!/bin/bash

# Путь к файлу, который нужно отслеживать
FILE="/home/dima/gits/TIMP/lab_3/part_a/sys.tat"

# Путь к вашему скрипту, который должен выполняться при открытии файла
SCRIPT="/home/dima/gits/TIMP/lab_3/part_a/directory_for_updating/secure.sh"

# Запускаем inotifywait для мониторинга открытия файла
inotifywait -m -e open "$FILE" | while read; do
    echo "[+] Файл $FILE был открыт. Запускаем защитный скрипт."
    ".$SCRIPT"
done