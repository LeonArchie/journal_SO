import csv
import json
import logging
import time

# Настройка логирования
logging.basicConfig(
    filename='log.log',  # Файл для записи логов
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)

# Функция для загрузки данных из CSV файла (в кодировке Windows-1251)
def load_replacements(csv_file):
    replacements = {}
    try:
        with open(csv_file, mode='r', encoding='windows-1251') as file:  # Указываем кодировку Windows-1251
            reader = csv.reader(file, delimiter=';')  # Используем точку с запятой как разделитель
            next(reader)  # Пропускаем первую строку
            for row in reader:
                if len(row) == 2:  # Проверяем, что есть два значения
                    old_value, new_value = row
                    replacements[old_value] = new_value
                    logging.info(f"Добавлена замена: '{old_value}' -> '{new_value}'")
                else:
                    logging.warning(f"Неправильный формат строки в файле {csv_file}: {row}")
        logging.info("Замены успешно загружены из файла.")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла {csv_file}: {e}")
        raise
    return replacements

# Функция для обновления JSON файла
def update_json(input_json_file, output_json_file, replacements):
    try:
        with open(input_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logging.info(f"Файл {input_json_file} успешно загружен.")

        # Проходим по всем классам и дням недели
        changes_made = False
        for class_name, days in data.items():
            for day, lessons in days.items():
                for lesson_number, lesson_info in lessons.items():
                    if 'lesson' in lesson_info:
                        original_lesson = lesson_info['lesson']
                        for old_value, new_value in replacements.items():
                            if old_value in lesson_info['lesson']:
                                lesson_info['lesson'] = lesson_info['lesson'].replace(old_value, new_value)
                                logging.info(f"Замена выполнена: класс={class_name}, день={day}, урок={lesson_number}, "
                                             f"'{original_lesson}' -> '{lesson_info['lesson']}'")
                                changes_made = True

        if not changes_made:
            logging.info("Нет изменений для применения.")

        # Сохраняем обновленные данные в новый файл
        with open(output_json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info(f"Обновленные данные успешно сохранены в файл {output_json_file}.")
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {input_json_file}: {e}")
        raise

# Основная часть скрипта
if __name__ == "__main__":
    logging.info("Скрипт начал работу.")
    time.sleep(2)
    try:
        # Загружаем замены из CSV файла (в кодировке Windows-1251)
        replacements = load_replacements('zamena.csv')
        
        # Обновляем JSON файл на основе замен и сохраняем в новый файл
        update_json('raspisanie_cab_updated.json', 'raspisanie_replace_lessons.json', replacements)
        logging.info("Скрипт успешно завершил работу.")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
    time.sleep(2)