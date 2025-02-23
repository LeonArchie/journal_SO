import json
import logging
from collections import OrderedDict
import os
import time

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_raspisanie(file_path):
    """Загружает данные из raspisanie_null_lesson_added.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.error("Файл raspisanie_null_lesson_added.json не найден")
        raise SystemExit("Файл raspisanie_null_lesson_added.json не найден")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла raspisanie_null_lesson_added.json: {e}")
        raise SystemExit(f"Ошибка при чтении файла raspisanie_null_lesson_added.json: {e}")

def sort_lessons(data):
    """Переставляет уроки в правильном порядке."""
    for class_name, days in data.items():
        logging.info(f"Сортировка уроков для класса: {class_name}")
        
        for day_name, lessons in days.items():
            new_lessons = OrderedDict()
            for key in sorted(lessons, key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else x):
                new_lessons[key] = lessons[key]
            days[day_name] = new_lessons
            logging.info(f"Обновленные данные для дня {day_name}: {new_lessons}")
    
    return data

if __name__ == "__main__":
    time.sleep(2)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'raspisanie_null_lesson_added.json')
    
    # Загрузка данных
    schedule_data = load_raspisanie(input_file_path)
    
    # Обработка данных
    updated_data = sort_lessons(schedule_data)
    
    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_sorted_schedule.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)