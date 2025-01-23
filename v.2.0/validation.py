import os
import csv
import sys
from datetime import datetime

def log_message(message, level):
    """
    Логирует сообщение с указанным уровнем и временем.
    Эта функция будет передана из journal_SO.py.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время
    log_entry = f"[{timestamp}] [{level}] {message}"  # Добавляем время в лог
    print(log_entry)  # Временный вывод в консоль для отладки

def validate_guide_file(file_path, log_message):
    """
    Проверяет файл Guide.csv на соответствие требованиям.
    :param file_path: Путь к файлу Guide.csv.
    :param log_message: Функция логирования.
    :return: Возвращает True, если файл валиден, иначе False.
    """
    try:
        log_message(f"Начало проверки файла Guide.csv: {file_path}", "INFO")

        # Проверка, что файл существует
        if not os.path.exists(file_path):
            log_message(f"Файл Guide.csv не найден: {file_path}", "ERROR")
            return False

        # Проверка, что файл не пустой
        if os.path.getsize(file_path) == 0:
            log_message("Файл Guide.csv пуст.", "ERROR")
            return False

        # Открываем файл для чтения
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            # Проверка первой строки
            if len(rows) < 1 or rows[0][0] != "Предметы":
                log_message("Первая строка файла Guide.csv не содержит слово 'Предметы'.", "ERROR")
                return False

            # Проверка второй строки
            if len(rows) < 2 or not rows[1]:
                log_message("Вторая строка файла Guide.csv пуста.", "ERROR")
                return False

        log_message("Файл Guide.csv валиден.", "INFO")
        return True

    except Exception as e:
        log_message(f"Ошибка при проверке файла Guide.csv: {e}", "ERROR")
        return False

def validate_schedule_file(file_path, log_message):
    """
    Проверяет файл Schedule.csv на соответствие требованиям.
    :param file_path: Путь к файлу Schedule.csv.
    :param log_message: Функция логирования.
    :return: Возвращает True, если файл валиден, иначе False.
    """
    try:
        log_message(f"Начало проверки файла Schedule.csv: {file_path}", "INFO")

        # Проверка, что файл существует
        if not os.path.exists(file_path):
            log_message(f"Файл Schedule.csv не найден: {file_path}", "ERROR")
            return False

        # Проверка, что файл не пустой
        if os.path.getsize(file_path) == 0:
            log_message("Файл Schedule.csv пуст.", "ERROR")
            return False

        # Открываем файл для чтения
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            # Проверка первой строки
            if len(rows) < 1 or "Расписание всех классов; Расписание каждого класса отдельно" not in rows[0][0]:
                log_message("Первая строка файла Schedule.csv не содержит ожидаемого текста.", "ERROR")
                return False

            # Проверка второй строки (ожидаемое значение: строка из запятых)
            if len(rows) < 2 or not all(cell == "" for cell in rows[1]):
                log_message("Вторая строка файла Schedule.csv не соответствует ожидаемому формату (ожидаются только запятые).", "ERROR")
                return False

            # Проверка третьей строки
            if len(rows) < 3 or "Расписание уроков для классов" not in rows[2][0]:
                log_message("Третья строка файла Schedule.csv не содержит ожидаемого текста.", "ERROR")
                return False

        log_message("Файл Schedule.csv валиден.", "INFO")
        return True

    except Exception as e:
        log_message(f"Ошибка при проверке файла Schedule.csv: {e}", "ERROR")
        return False

def main(schedule_file, reference_file, log_message):
    """
    Основная функция для проверки файлов Schedule.csv и Guide.csv.
    :param schedule_file: Путь к файлу Schedule.csv.
    :param reference_file: Путь к файлу Guide.csv.
    :param log_message: Функция логирования.
    :return: Возвращает True, если оба файла валидны, иначе False.
    """
    try:
        log_message(f"Начало работы скрипта Validation.py. Проверка файлов: {schedule_file}, {reference_file}", "INFO")

        # Проверка файла Guide.csv
        if not validate_guide_file(reference_file, log_message):
            log_message("Файл Guide.csv не валиден.", "ERROR")
            return False

        # Проверка файла Schedule.csv
        if not validate_schedule_file(schedule_file, log_message):
            log_message("Файл Schedule.csv не валиден.", "ERROR")
            return False

        # Если оба файла валидны
        log_message("Оба файла валидны.", "INFO")
        return True

    except Exception as e:
        log_message(f"Ошибка при выполнении скрипта Validation.py: {e}", "ERROR")
        return False

if __name__ == "__main__":
    # Пример вызова скрипта напрямую (для тестирования)
    def log_message(message, level):
        print(f"[{level}] {message}")

    # Получаем аргументы командной строки
    if len(sys.argv) != 3:
        print("Использование: python Validation.py <schedule_file> <reference_file>")
        sys.exit(1)

    schedule_file = sys.argv[1]
    reference_file = sys.argv[2]

    # Вызов основной функции
    result = main(schedule_file, reference_file, log_message)
    if result:
        print("Файлы валидны.")
    else:
        print("Файлы не валидны.")