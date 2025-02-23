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
    """Загружает данные из raspisanie.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)
        return data
    except FileNotFoundError:
        logging.error("Файл raspisanie.json не найден")
        raise SystemExit("Файл raspisanie.json не найден")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла raspisanie.json: {e}")
        raise SystemExit(f"Ошибка при чтении файла raspisanie.json: {e}")

def add_keys(data):
    """Обрабатывает ключи, заканчивающиеся на .1, чтобы они соответствовали формату previous_key.1."""
    for class_name, days in data.items():
        logging.info(f"Начинаем обработку класса: {class_name}")
        
        for day_name, lessons in days.items():
            logging.info(f"Начинаем обработку дня: {day_name}")
            
            new_lessons = OrderedDict()
            previous_key = None
            
            for key, lesson in lessons.items():
                logging.debug(f"Обработка урока с ключом: {key}")
                
                if key.isdigit():
                    # Если ключ числовой, обновляем previous_key
                    previous_key = key
                    logging.debug(f"Обновление previous_key на '{key}'")
                
                if key.endswith(".1"):
                    # Если ключ заканчивается на .1
                    if previous_key is not None:
                        expected_key = f"{previous_key}.1"
                        if key != expected_key:
                            # Если ключ не соответствует формату previous_key.1, изменяем его
                            logging.warning(f"Ключ {key} не соответствует формату '{expected_key}'. Исправляем.")
                            key = expected_key  # Изменяем ключ
                
                # Добавляем ключ и его значение в новый словарь
                new_lessons[key] = lesson
                logging.debug(f"Добавлен ключ {key} со значением {lesson}")
            
            # Заменяем старый словарь новым
            days[day_name] = new_lessons
            logging.info(f"Обновленные данные для дня {day_name}: {new_lessons}")
    
    return data

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'raspisanie.json')
    
    # Загрузка данных
    schedule_data = load_raspisanie(input_file_path)
    
    # Обработка данных
    updated_data = add_keys(schedule_data)
    
    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_key_added.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)