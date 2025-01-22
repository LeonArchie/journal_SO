import os
import time
import subprocess

# Функция для логирования
def log(message):
    """
    Логирует сообщение с временной меткой в консоль и в файл app.log.
    :param message: Сообщение для логирования.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время
    log_message = f"[{timestamp}] {message}"
    print(log_message)  # Выводим сообщение с временной меткой в консоль
    
    # Записываем сообщение в файл app.log
    with open("app.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")

# Функция для проверки наличия файла
def check_file(file_path, encoding='utf-8'):
    """
    Проверяет наличие файла и его кодировку.
    :param file_path: Путь к файлу.
    :param encoding: Кодировка файла (по умолчанию 'utf-8').
    :return: True, если файл существует и его кодировка корректна, иначе False.
    """
    log(f"Проверка файла: {file_path}")
    if not os.path.exists(file_path):  # Проверяем, существует ли файл
        log(f"Файл {file_path} не найден.")
        return False
    try:
        # Пытаемся открыть файл и прочитать его содержимое
        with open(file_path, 'r', encoding=encoding) as file:
            file.read()
        log(f"Файл {file_path} успешно проверен.")
        return True
    except UnicodeDecodeError:  # Если кодировка файла неверна
        log(f"Файл {file_path} имеет неверную кодировку.")
        return False

# Функция для запуска скрипта
def run_script(script_name):
    """
    Запускает внешний скрипт с помощью subprocess.
    :param script_name: Имя скрипта для запуска.
    :return: True, если скрипт выполнен успешно, иначе False.
    """
    log(f"Запуск скрипта: {script_name}")
    try:
        # Запускаем скрипт с помощью subprocess
        subprocess.run(["python3", script_name], check=True)
        log(f"Скрипт {script_name} успешно выполнен.")
        return True
    except subprocess.CalledProcessError as e:  # Если скрипт завершился с ошибкой
        log(f"Ошибка при выполнении скрипта {script_name}: {e}")
        return False

# Основной скрипт
def main():
    """
    Основная функция, которая управляет выполнением всех шагов.
    """
    # Пауза между шагами (3 секунды)
    pause_duration = 3
    log("Начало работы основного скрипта.")

    # 1. Проверка наличия файла Rasp.csv в кодировке Windows-1251
    log("Шаг 1: Проверка файла rasp.csv...")
    if not check_file('/home/archie/EDU/rasp.csv', encoding='windows-1251'):
        log("Файл Rasp.csv не найден или имеет неверную кодировку. Загрузка невозможна.")
        return
    log("Файл rasp.csv успешно проверен.")
    time.sleep(pause_duration)  # Пауза перед следующим шагом

    # 2. Запуск скрипта rasp_to_json.py
    log("Шаг 2: Запуск скрипта rasp_to_json.py...")
    if not run_script('/home/archie/EDU/rasp_to_json.py'):
        log("Ошибка при выполнении скрипта rasp_to_json.py. Загрузка невозможна.")
        return
    log("Скрипт rasp_to_json.py успешно выполнен.")
    time.sleep(pause_duration)

    # 3. Проверка файла Spravosh.csv
    log("Шаг 3: Проверка файла Spravosh.csv...")
    if not check_file('/home/archie/EDU/Spravosh.csv', encoding='cp1251'):
        log("Файл Spravosh.csv не найден или имеет неверную кодировку. Загрузка невозможна.")
        return
    log("Файл Spravosh.csv успешно проверен.")
    time.sleep(pause_duration)

    # 4. Запуск скрипта FindError.py
    log("Шаг 4: Запуск скрипта FindError.py...")
    if not run_script('/home/archie/EDU/FindError.py'):
        log("Ошибка при выполнении скрипта FindError.py. Загрузка невозможна.")
        return
    log("Скрипт FindError.py успешно выполнен.")
    time.sleep(pause_duration)

    # 5. Проверка наличия ошибок
    log("Шаг 5: Проверка наличия ошибок в расписании...")
    error_file_path = '/home/archie/EDU/error.txt'
    if os.path.exists(error_file_path):  # Проверяем, существует ли файл с ошибками
        with open(error_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if len(lines) > 1:  # Если файл содержит больше одной строки (заголовок + ошибки)
                log("ЕСТЬ ОШИБКИ В РАСПИСАНИИ. ЗАГРУЗКА НЕ ВОЗМОЖНА.")
                return
    log("Ошибок не найдено.")
    time.sleep(pause_duration)

    # 6. Запуск скрипта json_to_GIS_SO.py
    log("Шаг 6: Запуск скрипта json_to_GIS_SO.py...")
    if not run_script('/home/archie/EDU/json_to_GIS_SO.py'):
        log("Ошибка при выполнении скрипта json_to_GIS_SO.py. Загрузка невозможна.")
        return
    log("Скрипт json_to_GIS_SO.py успешно выполнен.")
    time.sleep(pause_duration)

    # 7. Завершение работы
    log("Шаг 7: Завершение работы.")
    log("Файл готов к загрузке. Можно забирать файл.")

# Точка входа в программу
if __name__ == "__main__":
    main()