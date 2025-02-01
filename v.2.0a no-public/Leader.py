import os
import subprocess
import shutil
from datetime import datetime
import sys

# Настройка логирования в файл
log_file = open("leader.log", "w", encoding="utf-8")

def log_message(message, level):
    """
    Логирует сообщение с указанным уровнем и временем.
    :param message: Сообщение для логирования.
    :param level: Уровень логирования (INFO, ERROR, DEBUG, OK и т.д.).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    # Записываем сообщение в файл
    log_file.write(log_entry + "\n")
    log_file.flush()  # Обеспечиваем запись в файл сразу

def run_script(script_name, log_message, *args):
    """
    Запускает внешний скрипт с помощью subprocess.Popen и передает вывод в реальном времени.
    :param script_name: Имя скрипта для запуска.
    :param log_message: Функция логирования.
    :param args: Аргументы для скрипта.
    :return: True, если скрипт выполнен успешно, иначе False.
    """
    log_message(f"Запуск скрипта: {script_name}", "INFO")
    try:
        # Запускаем процесс с Popen
        process = subprocess.Popen(
            ["python", script_name, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Построчная буферизация
            universal_newlines=True
        )

        # Читаем вывод в реальном времени
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log_message(f"[{script_name}] {output.strip()}", "DEBUG")

            error = process.stderr.readline()
            if error:
                log_message(f"[{script_name}] {error.strip()}", "ERROR")

        # Ожидаем завершения процесса
        process.wait()

        if process.returncode == 0:
            log_message(f"Скрипт {script_name} успешно выполнен.", "OK")
            return True
        else:
            log_message(f"Скрипт {script_name} завершился с ошибкой. Код возврата: {process.returncode}", "ERROR")
            return False

    except Exception as e:
        log_message(f"Ошибка при выполнении скрипта {script_name}: {e}", "ERROR")
        return False

def convert_or_move_files(schedule_file, reference_file, log_message):
    """
    Преобразует Excel-файлы в CSV или перекладывает CSV-файлы в папку с программой.
    :param schedule_file: Путь к файлу расписания.
    :param reference_file: Путь к файлу справочника.
    :param log_message: Функция логирования.
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
        log_message(f"Файл расписания {schedule_file} уже в формате CSV. Начинаем перекладывание в папку с программой.", "INFO")
        try:
            shutil.copy(schedule_file, csv_schedule_file)
            log_message(f"Файл расписания успешно переложен в: {csv_schedule_file}", "OK")
        except Exception as e:
            log_message(f"Ошибка при перекладывании файла расписания: {e}", "ERROR")
            return None
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
        log_message(f"Файл справочника {reference_file} уже в формате CSV. Начинаем перекладывание в папку с программой.", "INFO")
        try:
            shutil.copy(reference_file, csv_reference_file)
            log_message(f"Файл справочника успешно переложен в: {csv_reference_file}", "OK")
        except Exception as e:
            log_message(f"Ошибка при перекладывании файла справочника: {e}", "ERROR")
            return None
    else:
        log_message(f"Файл справочника {reference_file} имеет неверный формат. Ожидается .xlsx или .csv.", "ERROR")
        return None

    # Проверка наличия файлов после преобразования или перекладывания
    log_message("Проверка наличия файлов после преобразования или перекладывания...", "DEBUG")
    if not os.path.exists(csv_schedule_file):
        log_message(f"Файл расписания {csv_schedule_file} отсутствует после преобразования или перекладывания.", "ERROR")
        return None
    if not os.path.exists(csv_reference_file):
        log_message(f"Файл справочника {csv_reference_file} отсутствует после преобразования или перекладывания.", "ERROR")
        return None

    log_message("Файлы успешно преобразованы или переложены.", "OK")  # Уровень OK для успешного завершения
    return csv_schedule_file, csv_reference_file

def main(schedule_file, reference_file, log_message):
    """
    Основная функция, которая управляет выполнением всех шагов.
    :param schedule_file: Путь к файлу расписания.
    :param reference_file: Путь к файлу справочника.
    :param log_message: Функция логирования.
    """
    log_message("Начало работы основного скрипта.", "INFO")
    log_message("Запуск скрипта Leader.py...", "OK")  # Логирование запуска скрипта

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

    log_message("JSON-файл успешно создан. Работа скрипта завершена.", "OK")  # Уровень OK для успешного завершения

# Точка входа в программу
if __name__ == "__main__":
    # Получаем аргументы командной строки
    if len(sys.argv) != 3:
        print("Использование: python Leader.py <schedule_file> <reference_file>")
        sys.exit(1)

    # Пути к файлам (должны быть переданы из journal_SO.py)
    schedule_file = sys.argv[1]  # Путь к файлу расписания
    reference_file = sys.argv[2]  # Путь к файлу справочника

    # Вызов основной функции
    main(schedule_file, reference_file, log_message)