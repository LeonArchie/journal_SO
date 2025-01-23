import os
import pandas as pd
import sys
from datetime import datetime

def log_message(message, level):
    """
    Логирует сообщение с указанным уровнем и временем.
    :param message: Сообщение для логирования.
    :param level: Уровень логирования (INFO, ERROR, DEBUG, OK и т.д.).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    # Вывод в stdout для INFO, DEBUG, OK и в stderr для ERROR
    if level == "ERROR":
        print(log_entry, file=sys.stderr)
    else:
        print(log_entry, file=sys.stdout)
    return timestamp, level, message

def excel_to_csv(excel_file, csv_file, log_message):
    """
    Преобразует Excel-файл в CSV.

    :param excel_file: Путь к Excel-файлу.
    :param csv_file: Путь для сохранения CSV-файла.
    :param log_message: Функция логирования, переданная из journal_SO.pyw.
    """
    try:
        log_message(f"Начало преобразования файла {excel_file} в CSV...", "INFO")
        df = pd.read_excel(excel_file)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        log_message(f"Файл успешно преобразован: {csv_file}", "OK")  # Уровень OK для успешного преобразования
    except Exception as e:
        log_message(f"Ошибка при преобразовании файла: {e}", "ERROR")
        raise  # Пробрасываем исключение для обработки в вызывающем коде

def check_and_convert_files(schedule_file, reference_file, log_message):
    """
    Проверяет типы файлов и преобразует Excel в CSV, если это необходимо.

    :param schedule_file: Путь к файлу расписания.
    :param reference_file: Путь к файлу справочника.
    :param log_message: Функция логирования из основного скрипта.
    :return: Возвращает пути к файлам (оригинальные или преобразованные).
    """
    try:
        # Логирование начала процесса проверки файлов
        log_message("Начало проверки и преобразования файлов.", "INFO")
        log_message(f"Полученные пути: schedule_file = {schedule_file}, reference_file = {reference_file}", "DEBUG")

        # Получаем текущую директорию, где находится скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_message(f"Текущая директория скрипта: {script_dir}", "DEBUG")

        # Проверка существования файла расписания
        log_message("Проверка существования файла расписания...", "DEBUG")
        if not os.path.exists(schedule_file):
            log_message(f"Файл расписания {schedule_file} не найден.", "ERROR")
            raise FileNotFoundError(f"Файл расписания {schedule_file} не найден.")
        log_message(f"Файл расписания {schedule_file} существует.", "DEBUG")

        # Проверка и преобразование файла расписания
        log_message("Проверка типа файла расписания...", "DEBUG")
        if schedule_file.endswith('.xlsx'):
            log_message(f"Обнаружен Excel-файл расписания: {schedule_file}. Начинаем преобразование в CSV.", "INFO")
            
            # Формируем путь для CSV-файла в той же директории, что и скрипт
            schedule_filename = os.path.basename(schedule_file).replace('.xlsx', '.csv')
            csv_schedule_file = os.path.join(script_dir, schedule_filename)
            log_message(f"Сформирован путь для CSV-файла расписания: {csv_schedule_file}", "DEBUG")

            # Проверка существования CSV-файла перед преобразованием
            if os.path.exists(csv_schedule_file):
                log_message(f"CSV-файл расписания {csv_schedule_file} уже существует. Удаление старого файла.", "INFO")
                os.remove(csv_schedule_file)
                log_message(f"Старый CSV-файл расписания {csv_schedule_file} удален.", "DEBUG")

            # Преобразование Excel в CSV
            log_message(f"Вызов функции excel_to_csv для файла расписания: {schedule_file}", "DEBUG")
            excel_to_csv(schedule_file, csv_schedule_file, log_message)  # Передаем log_message
            log_message(f"Excel-файл расписания успешно преобразован в CSV: {csv_schedule_file}", "OK")  # Уровень OK для успешного преобразования

            # Обновление пути к файлу расписания
            schedule_file = csv_schedule_file
            log_message(f"Обновленный путь к файлу расписания: {schedule_file}", "DEBUG")
        else:
            log_message(f"Файл расписания {schedule_file} уже в формате CSV. Преобразование не требуется.", "INFO")

        # Проверка существования файла справочника
        log_message("Проверка существования файла справочника...", "DEBUG")
        if not os.path.exists(reference_file):
            log_message(f"Файл справочника {reference_file} не найден.", "ERROR")
            raise FileNotFoundError(f"Файл справочника {reference_file} не найден.")
        log_message(f"Файл справочника {reference_file} существует.", "DEBUG")

        # Проверка и преобразование файла справочника
        log_message("Проверка типа файла справочника...", "DEBUG")
        if reference_file.endswith('.xlsx'):
            log_message(f"Обнаружен Excel-файл справочника: {reference_file}. Начинаем преобразование в CSV.", "INFO")
            
            # Формируем путь для CSV-файла в той же директории, что и скрипт
            reference_filename = os.path.basename(reference_file).replace('.xlsx', '.csv')
            csv_reference_file = os.path.join(script_dir, reference_filename)
            log_message(f"Сформирован путь для CSV-файла справочника: {csv_reference_file}", "DEBUG")

            # Проверка существования CSV-файла перед преобразованием
            if os.path.exists(csv_reference_file):
                log_message(f"CSV-файл справочника {csv_reference_file} уже существует. Удаление старого файла.", "INFO")
                os.remove(csv_reference_file)
                log_message(f"Старый CSV-файл справочника {csv_reference_file} удален.", "DEBUG")

            # Преобразование Excel в CSV
            log_message(f"Вызов функции excel_to_csv для файла справочника: {reference_file}", "DEBUG")
            excel_to_csv(reference_file, csv_reference_file, log_message)  # Передаем log_message
            log_message(f"Excel-файл справочника успешно преобразован в CSV: {csv_reference_file}", "OK")  # Уровень OK для успешного преобразования

            # Обновление пути к файлу справочника
            reference_file = csv_reference_file
            log_message(f"Обновленный путь к файлу справочника: {reference_file}", "DEBUG")
        else:
            log_message(f"Файл справочника {reference_file} уже в формате CSV. Преобразование не требуется.", "INFO")

        # Логирование успешного завершения
        log_message("Проверка и преобразование файлов завершены успешно.", "OK")  # Уровень OK для успешного завершения
        log_message(f"Итоговые пути: schedule_file = {schedule_file}, reference_file = {reference_file}", "DEBUG")

        return schedule_file, reference_file

    except Exception as e:
        # Логирование ошибки
        log_message(f"Ошибка при проверке и преобразовании файлов: {e}", "ERROR")
        log_message(f"Текущие пути: schedule_file = {schedule_file}, reference_file = {reference_file}", "DEBUG")
        raise  # Пробрасываем исключение дальше для обработки в основном скрипте