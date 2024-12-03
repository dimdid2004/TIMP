from settings import pathToTemplates, data
import json
import os
import stat
import sys
import hashlib
# импорт partial для фиксирования аргументов и, как следствие, контекста функции 
from functools import partial

#импорт классов монитоинга за изменениями в ФС и обработчика событий изменения
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
import signal

#Класс для защиты от удаления программного файла 
class ProtectedFileHandler(FileSystemEventHandler):
    def __init__(self, filename, handler):
        self.protectedFileName = filename
        self.handler = handler
    def on_deleted(self, event):
        # Получаем имя файла без пути
        fileName = os.path.basename(event.src_path)
        if fileName == self.protectedFileName:
            print(f"\n[WARNING] File '{self.protectedFileName}' can't be deleted!\n[+] >> ", end = '')
            #Восстанавливаем файл из резервной копии или создаем новый
            self.handler()



class AppData:
    def __init__(self, pathToTemplates):
        global data
        self.dataFile = pathToTemplates
        if (not self._fileExists()):
            self._writeDataFile(data)
        self.hashedPwd = self._getPassword()
        self.restrictedList = self.getTemplates()
        eventHandler = ProtectedFileHandler(self.dataFile, partial(self._restorePathToTemplate))
        self.protectedObserver = Observer()
        self.protectedObserver.schedule(eventHandler, os.getcwd(), recursive=False)

    def _fileExists(self):
        return os.path.isfile(self.dataFile)
    def _readDataFile(self):
        with open(self.dataFile, "r") as fileWithTemplates:
            data = json.load(fileWithTemplates)
        return data
    def _writeDataFile(self, data):
        with open(self.dataFile, 'w', encoding='utf-8') as fileWithPwd:
            json.dump(data, fileWithPwd, ensure_ascii=False, indent=4)
    def _setPassword(self):
        # просим пароль пользователя
        pwdFromUser = ''
        while pwdFromUser == '':
            pwdFromUser = input("[pwd] >> ")
            if pwdFromUser == '':
                print("[pwd] Password cannot be empty")
        self.hashedPwd = hashlib.md5(pwdFromUser.encode()).hexdigest()
        data = self._readDataFile()
        data['password'] = self.hashedPwd
        self._writeDataFile(data)


    def _getPassword(self):
        return self._readDataFile()['password']

    def _restorePathToTemplate(self):
        global data
        data['password'] = self.hashedPwd
        data['files'] = self.restrictedList
        self._writeDataFile(data)

    def checkPassword(self):
        print("[pwd] Enter the password")
        pwd = input("[pwd] >> ")
        hashedPwd = hashlib.md5(pwd.encode()).hexdigest()
        return hashedPwd == self._getPassword()

    # можно доработать
    def setRestricts(self):
        while True:
            print("[policy] Enter the names of the files to which you want to apply the security policy")
            print("Ex: file1, file2, file3")
            strFromUser = input("[policy] >> ").strip()

            # Проверяем, что строка не пустая
            if strFromUser:
                # Удаляем пробелы и разбиваем по запятым
                fileNames = [name.strip() for name in strFromUser.split(',')]

                # Проверяем, что есть хотя бы одно имя файла
                if all(name for name in fileNames):
                    os.chmod(self.dataFile, stat.S_IWRITE | stat.S_IREAD)
                    data = self._readDataFile()
                    data['files'] += fileNames
                    self._writeDataFile(data)
                    self.restrictedList = self.getTemplates()
                    os.chmod(self.dataFile, stat.S_IREAD)
                    print(f"[policy] Files '{fileNames}' successfully was added to restriction list")
                    return
                else:
                    print("Ошибка: каждый элемент должен быть непустой строкой. Пожалуйста, попробуйте снова.")
            else:
                print("Ошибка: входная строка не должна быть пустой. Пожалуйста, попробуйте снова.")

    def isPasswordSet(self):
        if self._getPassword() == "":
            #Пользователь не установил пароль -> просим его это сделать
            print("[pwd] Before first use of applicetion your should set app a password for closing applicaion")
            self._setPassword()
            print("[policy] Would you like to expand the list of protected files? (Yes/No)")
            response = ''
            while response.lower() != 'yes' and response.lower() != 'no':
                response = input("[policy] >> ")
                if response.lower() != 'yes' and response.lower() != 'no':
                    print("[policy] Please enter 'Yes' or 'No'")
            if response.lower() == 'yes':
                self.setRestricts()
            #Разрешаем только читать системный файл
            os.chmod(self.dataFile, stat.S_IREAD)  
            #И не даем его удалить
            self.protectedObserver.start()
            return False
        else:
            os.chmod(self.dataFile, stat.S_IREAD) 
            self.protectedObserver.start()
            return True
    def getTemplates(self):
        return self._readDataFile()['files']

    def __exit__():
        if self.protectedObserver != None:
            self.protectedObserver.stop()

appData = AppData(pathToTemplates)

def try_to_remove_file(file_path):
    while True:
        try:
            os.remove(file_path)
            print(f"\n[INFO] Successfully removed '{file_path}'\n[+] >> ", end="")
            break  # Успешное удаление, выходим из цикла
        except PermissionError:
            print(f"[WARNING] Permission denied for '{file_path}'. Retrying in 1 second...")
            time.sleep(1)  # Ждем 1 секунду перед повторной попыткой






class ForbiddenFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global appData
        # скипаем директории
        if os.path.isdir(event.src_path):
            return
        # Получаем имя файла без пути
        file_name = os.path.basename(event.src_path)
        # Реагируем на все файлы с запрещенными именами (вне зависимости от их расширения)
        if any(forbidden_name in file_name for forbidden_name in appData.getTemplates()):
            print(f"\n[DEFENDER] Want to create file with forbidden filename: {file_name}\n[+] >> ", end='')
            try_to_remove_file(event.src_path)


    # Обработка переименования или перемещения файла
    def on_moved(self, event):
        global appData
        # скипаем директории
        if os.path.isdir(event.src_path):
            return
        file_name = os.path.basename(event.dest_path)
        if any(forbidden_name in file_name for forbidden_name in appData.getTemplates()):
            print(f"\n[DEFENDER] Want to rename to forbidden filename: {file_name}\n[+] >> ", end='')
            try_to_remove_file(event.dest_path)

# Создаем обработчик событий и наблюдателя
event_handler = ForbiddenFileHandler()
observer = Observer()
observer.schedule(event_handler, os.getcwd(), recursive=False)
def info():
    print("[+] Possible commands: ")
    print("    'start' - starts to defend current directory")
    print("    'stop' - stops to defend current directory")
    print("    'exit' - leave the app")
    print("    'info' - info about the app")

def start():
    global appData

    # Избегаем ошибок пользовательского ввода
    if not hasattr(start, 'call_count'):
        start.call_count = 0  # инициализация счётчика

    if start.call_count >= 1:
        print("[-] You've alreade started defending => enter 'stop' to leave the app")
        return

    if (not appData.checkPassword()):
        print("[pwd] Password is wrong")
        return


    print("[DEFENDER] Protection is on")
    observer.start()

    start.call_count += 1

def append():
    global appData
    appData.setRestricts()

def stop():
    global appData
    if (not appData.checkPassword()):
        print("[pwd] Password is wrong")
        return
    print("[DEFENDER] Protection is off")
    observer.stop()
    sys.exit(0)



###


if __name__ == "__main__":
    print("    ---- Security Manager For Current Directory ----")

    appData.isPasswordSet()

    possibleCommands = {
        "start": start,
        "stop": stop,
        "append": append,
        "info": info
    }

    print("[+] Enter (start/stop/append/info)")
    while True:
        try:
            userCommand = input("[+] >> ")
            possibleCommands.get(userCommand, lambda: print("[-] Unknown command"))()
        except (KeyboardInterrupt, EOFError, UnicodeDecodeError):
            print("\n[pwd] You should enter a password to finish the program")
            if appData.checkPassword():
                break
            print("[pwd] Password is wrong")








