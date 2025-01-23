import os
import time
import subprocess
import shutil

def check_file(file_path, log_message, encoding='utf-8'):
    """
    Проверяет наличие файла и его кодировку.
    :param file_path: Путь к файлу.
    :param log_message: Функция логирования из journal_SO.pyw.
    :param encoding: Кодировка файла (по умолчанию 'utf-8').
    :return: True, если файл существует и его кодировка корректна, иначе False.
    """
    log_message(f"Проверка файла: {file_path}", "DEBUG")
    if not os.path.exists(file_path):
        log_message(f"Файл {file_path} не найден.", "ERROR")
        return False
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            file.read()
        log_message(f"Файл {file_path} успешно проверен.", "DEBUG")
        return True
    except UnicodeDecodeError:
        log_message(f"Файл {file_path} имеет неверную кодировку.", "ERROR")
        return False

def run_script(script_name, log_message, *args):
    """
    Запускает внешний скрипт с помощью subprocess.
    :param script_name: Имя скрипта для запуска.
    :param log_message: Функция логирования из journal_SO.pyw.
    :param args: Аргументы для скрипта.
    :return: True, если скрипт выполнен успешно, иначе False.
    """
    log_message(f"Запуск скрипта: {script_name}", "INFO")
    try:
        subprocess.run(["python", script_name, *args], check=True)
        log_message(f"Скрипт {script_name} успешно выполнен.", "INFO")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Ошибка при выполнении скрипта {script_name}: {e}", "ERROR")
        return False

def convert_or_move_files(schedule_file, reference_file, log_message):
    """
    Преобразует Excel-файлы в CSV или перекладывает CSV-файлы в папку с программой.
    :param schedule_file: Путь к файлу расписания.
    :param reference_file: Путь к файлу справочника.
    :param log_message: Функция логирования из journal_SO.pyw.
    :return: Возвращает пути к CSV-файлам или None, если произошла ошибка.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_message(f"Текущая директория скрипта: {script_dir}", "DEBUG")

    csv_schedule_file = os.path.join(script_dir, "Schedule.csv")
    csv_reference_file = os.path.join(script_dir, "Guide.csv")

    # Обработка файла расписания
    if schedule_file.endswith('.xlsx'):
        log_message(f"Обнаружен Excel-файл расписания: {schedule_file}. Начинаем преобразование в CSV.", "INFO")
        if not run_script("excel_to_csv.py", log_message, schedule_file, csv_schedule_file):
            log_message("Ошибка при преобразовании файла расписания в CSV.", "ERROR")
            return None
    elif schedule_file.endswith('.csv'):
        log_message(f"Файл расписания {schedule_file} уже в формате CSV. Перекладываем в папку с программой.", "INFO")
        shutil.copy(schedule_file, csv_schedule_file)
    else:
        log_message(f"Файл расписания {schedule_file} имеет неверный формат. Ожидается .xlsx или .csv.", "ERROR")
        return None

    # Обработка файла справочника
    if reference_file.endswith('.xlsx'):
        log_message(f"Обнаружен Excel-файл справочника: {reference_file}. Начинаем преобразование в CSV.", "INFO")
        if not run_script("excel_to_csv.py", log_message, reference_file, csv_reference_file):
            log_message("Ошибка при преобразовании файла справочника в CSV.", "ERROR")
            return None
    elif reference_file.endswith('.csv'):
        log_message(f"Файл справочника {reference_file} уже в формате CSV. Перекладываем в папку с программой.", "INFO")
        shutil.copy(reference_file, csv_reference_file)
    else:
        log_message(f"Файл справочника {reference_file} имеет неверный формат. Ожидается .xlsx или .csv.", "ERROR")
        return None

    # Проверка наличия файлов после преобразования или перекладывания
    if not os.path.exists(csv_schedule_file) or not os.path.exists(csv_reference_file):
        log_message("Один или оба файла отсутствуют после преобразования или перекладывания.", "ERROR")
        return None

    log_message("Файлы успешно преобразованы или переложены.", "INFO")
    return csv_schedule_file, csv_reference_file

def main(schedule_file, reference_file, log_message):
    """
    Основная функция, которая управляет выполнением всех шагов.
    :param schedule_file: Путь к файлу расписания.
    :param reference_file: Путь к файлу справочника.
    :param log_message: Функция логирования из journal_SO.pyw.
    """
    log_message("Начало работы основного скрипта.", "INFO")

    # 1. Преобразование Excel в CSV или перекладывание CSV-файлов
    log_message("Шаг 1: Преобразование или перекладывание файлов...", "INFO")
    result = convert_or_move_files(schedule_file, reference_file, log_message)
    if not result:
        log_message("Ошибка при преобразовании или перекладывании файлов. Завершение работы.", "ERROR")
        return
    csv_schedule_file, csv_reference_file = result

    # 2. Проверка валидности файлов с помощью скрипта Validation.py
    log_message("Шаг 2: Проверка валидности файлов...", "INFO")
    if not run_script("Validation.py", log_message, csv_schedule_file, csv_reference_file):
        log_message("Файлы не валидны. Завершение работы.", "ERROR")
        return

    # 3. Запуск скрипта avers_csv_to_json.py
    log_message("Шаг 3: Запуск скрипта avers_csv_to_json.py...", "INFO")
    if not run_script("avers_csv_to_json.py", log_message, csv_schedule_file):
        log_message("Ошибка при выполнении скрипта avers_csv_to_json.py. Завершение работы.", "ERROR")
        return

    # 4. Проверка наличия JSON-файла
    json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Schedule.json")
    if not os.path.exists(json_file_path):
        log_message("JSON-файл не создан. Завершение работы.", "ERROR")
        return

    log_message("JSON-файл успешно создан. Работа скрипта завершена.", "INFO")

# Точка входа в программу
if __name__ == "__main__":
    # Пример вызова скрипта напрямую (для тестирования)
    def log_message(message, level="INFO"):
        print(f"[{level}] {message}")

    # Пути к файлам (должны быть переданы из journal_SO.py)
    schedule_file = "path/to/Schedule.xlsx"  # Укажите путь к файлу расписания
    reference_file = "path/to/Guide.xlsx"    # Укажите путь к файлу справочника

    # Вызов основной функции
    main(schedule_file, reference_file, log_message)