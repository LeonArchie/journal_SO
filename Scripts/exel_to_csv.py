import os
import logging
import pandas as pd
import time

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Функция для проверки наличия файлов
def check_files(file_list):
    for file in file_list:
        if not os.path.exists(file):
            logging.error(f"Файл {file} не найден.")
            return False
    return True

# Функция для преобразования Excel в CSV
def convert_excel_to_csv(file_name):
    try:
        # Читаем Excel файл
        df = pd.read_excel(file_name)
        # Создаем имя CSV файла
        csv_file_name = file_name.replace('.xlsx', '.csv').replace('.xls', '.csv')
        # Сохраняем DataFrame в CSV с точкой с запятой как разделителем и кодировкой Windows-1251
        df.to_csv(csv_file_name, sep=';', index=False, encoding='windows-1251')
        logging.info(f"Файл {file_name} успешно преобразован в {csv_file_name}.")
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {file_name}: {e}")

# Основной скрипт
if __name__ == "__main__":
    time.sleep(2)
    logging.info("Скрипт начал выполнение.")

    # Список файлов для проверки
    files = ['raspisanie.xlsx', 'klass.xlsx', 'lesson.xlsx', 'groups.xlsx', 'zamena.xlsx']

    # Проверяем наличие файлов
    if not check_files(files):
        logging.info("Скрипт завершил работу из-за отсутствия файлов.")
        exit()

    # Преобразуем каждый файл Excel в CSV
    for file in files:
        convert_excel_to_csv(file)
        time.sleep(2)
    logging.info("Скрипт успешно завершил выполнение.")