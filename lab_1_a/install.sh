#!/usr/bin/bash
echo " --- Вас приветсвует Мастер установки программы 'Security_manager' ---"

VENV=".venv"
if [ ! -d "${VENV}" ]; then
    echo "Создаем виртуальное окружение с требуемыми зависимостями ..."
    python -m venv "$VENV"

    source "$VENV/bin/activate"

    pip install -r requirements.txt

    echo -e "\n\n"
fi

PROG_DIR=$(pwd)

pyinstaller --onefile security_manager.py --distpath "${PROG_DIR}"

# Устанавливаем права на исполняемый файл
chmod +x "${PROG_DIR}/security_manager"


rm -rf build/ security_manager.spec

echo "Установка успешно завершена."
