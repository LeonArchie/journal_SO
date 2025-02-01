import os
import pandas as pd
import sys
from datetime import datetime

# Настройка логирования в файл
log_file = open("excel_to_csv.log", "w", encoding="utf-8")

def log_message(message, level="INFO"):
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

def excel_to_csv(excel_file, csv_file, log_message):
    """
    Преобразует Excel-файл в CSV.

    :param excel_file: Путь к Excel-файлу.
    :param csv_file: Путь для сохранения CSV-файла.
    :param log_message: Функция логирования.
    """
    try:
        log_message(f"Начало преобразования файла {excel_file} в CSV...", "INFO")
        
        # Проверка, что Excel-файл существует
        if not os.path.exists(excel_file):
            log_message(f"Файл {excel_file} не найден.", "ERROR")
            raise FileNotFoundError(f"Файл {excel_file} не найден.")

        log_message(f"Чтение Excel-файла: {excel_file}", "DEBUG")
        
        # Чтение Excel-файла
        df = pd.read_excel(excel_file)
        log_message(f"Excel-файл успешно прочитан. Количество строк: {len(df)}", "DEBUG")
        
        log_message(f"Сохранение в CSV: {csv_file}", "DEBUG")
        
        # Сохранение в CSV
        df.to_csv(csv_file, index=False, encoding='utf-8')
        
        # Проверка, что CSV-файл создан
        if os.path.exists(csv_file):
            log_message(f"Файл успешно преобразован: {csv_file}", "OK")
        else:
            log_message(f"Файл {csv_file} не был создан.", "ERROR")
            raise Exception(f"Файл {csv_file} не был создан.")

    except Exception as e:
        log_message(f"Ошибка при преобразовании файла: {e}", "ERROR")
        raise  # Пробрасываем исключение для обработки в вызывающем коде

# Точка входа в программу
if __name__ == "__main__":
    # Получаем аргументы командной строки
    if len(sys.argv) != 3:
        log_message("Использование: python excel_to_csv.py <excel_file> <csv_file>", "ERROR")
        sys.exit(1)

    excel_file = sys.argv[1]  # Путь к Excel-файлу
    csv_file = sys.argv[2]    # Путь для сохранения CSV-файла

    # Вызов основной функции
    excel_to_csv(excel_file, csv_file, log_message)