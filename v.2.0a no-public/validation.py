import os
import csv
import sys
from datetime import datetime

# Настройка логирования в файл
log_file = open("validation.log", "w", encoding="utf-8")

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

def validate_guide_file(file_path, log_message):
    """
    Проверяет файл Guide.csv на соответствие требованиям.
    :param file_path: Путь к файлу Guide.csv.
    :param log_message: Функция логирования.
    :return: Возвращает True, если файл валиден, иначе False.
    """
    try:
        log_message(f"Начало проверки файла Guide.csv: {file_path}", "INFO")
        log_message(f"Проверка существования файла Guide.csv...", "DEBUG")

        # Проверка, что файл существует
        if not os.path.exists(file_path):
            log_message(f"Файл Guide.csv не найден: {file_path}", "ERROR")
            return False
        log_message(f"Файл Guide.csv найден: {file_path}", "DEBUG")

        # Проверка, что файл не пустой
        log_message(f"Проверка, что файл Guide.csv не пустой...", "DEBUG")
        if os.path.getsize(file_path) == 0:
            log_message("Файл Guide.csv пуст.", "ERROR")
            return False
        log_message("Файл Guide.csv не пуст.", "DEBUG")

        # Открываем файл для чтения
        log_message(f"Открытие файла Guide.csv для чтения...", "DEBUG")
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            log_message(f"Файл Guide.csv успешно прочитан. Количество строк: {len(rows)}", "DEBUG")

            # Проверка первой строки
            log_message(f"Проверка первой строки файла Guide.csv...", "DEBUG")
            if len(rows) < 1:
                log_message("Файл Guide.csv не содержит ни одной строки.", "ERROR")
                return False
            if rows[0][0] != "Предметы":
                log_message(f"Первая строка файла Guide.csv не содержит слово 'Предметы'. Найдено: {rows[0][0]}", "ERROR")
                return False
            log_message("Первая строка файла Guide.csv содержит слово 'Предметы'.", "DEBUG")

            # Проверка второй строки
            log_message(f"Проверка второй строки файла Guide.csv...", "DEBUG")
            if len(rows) < 2:
                log_message("Файл Guide.csv содержит менее двух строк.", "ERROR")
                return False
            if not rows[1]:
                log_message("Вторая строка файла Guide.csv пуста.", "ERROR")
                return False
            log_message("Вторая строка файла Guide.csv не пуста.", "DEBUG")

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
        log_message(f"Проверка существования файла Schedule.csv...", "DEBUG")

        # Проверка, что файл существует
        if not os.path.exists(file_path):
            log_message(f"Файл Schedule.csv не найден: {file_path}", "ERROR")
            return False
        log_message(f"Файл Schedule.csv найден: {file_path}", "DEBUG")

        # Проверка, что файл не пустой
        log_message(f"Проверка, что файл Schedule.csv не пустой...", "DEBUG")
        if os.path.getsize(file_path) == 0:
            log_message("Файл Schedule.csv пуст.", "ERROR")
            return False
        log_message("Файл Schedule.csv не пуст.", "DEBUG")

        # Открываем файл для чтения
        log_message(f"Открытие файла Schedule.csv для чтения...", "DEBUG")
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            log_message(f"Файл Schedule.csv успешно прочитан. Количество строк: {len(rows)}", "DEBUG")

            # Проверка первой строки
            log_message(f"Проверка первой строки файла Schedule.csv...", "DEBUG")
            if len(rows) < 1:
                log_message("Файл Schedule.csv не содержит ни одной строки.", "ERROR")
                return False
            if "Расписание всех классов; Расписание каждого класса отдельно" not in rows[0][0]:
                log_message(f"Первая строка файла Schedule.csv не содержит ожидаемого текста. Найдено: {rows[0][0]}", "ERROR")
                return False
            log_message("Первая строка файла Schedule.csv содержит ожидаемый текст.", "DEBUG")

            # Проверка второй строки
            log_message(f"Проверка второй строки файла Schedule.csv...", "DEBUG")
            if len(rows) < 2:
                log_message("Файл Schedule.csv содержит менее двух строк.", "ERROR")
                return False
            if not all(cell == "" for cell in rows[1]):
                log_message("Вторая строка файла Schedule.csv не соответствует ожидаемому формату (ожидаются только запятые).", "ERROR")
                return False
            log_message("Вторая строка файла Schedule.csv соответствует ожидаемому формату.", "DEBUG")

            # Проверка третьей строки
            log_message(f"Проверка третьей строки файла Schedule.csv...", "DEBUG")
            if len(rows) < 3:
                log_message("Файл Schedule.csv содержит менее трех строк.", "ERROR")
                return False
            if "Расписание уроков для классов" not in rows[2][0]:
                log_message(f"Третья строка файла Schedule.csv не содержит ожидаемого текста. Найдено: {rows[2][0]}", "ERROR")
                return False
            log_message("Третья строка файла Schedule.csv содержит ожидаемый текст.", "DEBUG")

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
        log_message("Запуск скрипта Validation.py...", "OK")  # Логирование запуска скрипта

        # Проверка файла Guide.csv
        log_message("Начало проверки файла Guide.csv...", "INFO")
        if not validate_guide_file(reference_file, log_message):
            log_message("Файл Guide.csv не валиден.", "ERROR")
            return False
        log_message("Файл Guide.csv успешно проверен и валиден.", "INFO")

        # Проверка файла Schedule.csv
        log_message("Начало проверки файла Schedule.csv...", "INFO")
        if not validate_schedule_file(schedule_file, log_message):
            log_message("Файл Schedule.csv не валиден.", "ERROR")
            return False
        log_message("Файл Schedule.csv успешно проверен и валиден.", "INFO")

        # Если оба файла валидны
        log_message("Оба файла (Schedule.csv и Guide.csv) валидны.", "OK")  # Уровень OK для успешного завершения
        return True

    except Exception as e:
        log_message(f"Ошибка при выполнении скрипта Validation.py: {e}", "ERROR")
        return False

# Точка входа в программу
if __name__ == "__main__":
    # Получаем аргументы командной строки
    if len(sys.argv) != 3:
        log_message("Использование: python Validation.py <schedule_file> <reference_file>", "ERROR")
        sys.exit(1)

    schedule_file = sys.argv[1]
    reference_file = sys.argv[2]

    # Вызов основной функции
    result = main(schedule_file, reference_file, log_message)
    if result:
        log_message("Файлы валидны.", "OK")
    else:
        log_message("Файлы не валидны.", "ERROR")