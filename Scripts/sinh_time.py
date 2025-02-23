import json
import logging
import os
import time

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_raspisanie(file_path):
    """Загружает данные из raspisanie_key_added.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.error("Файл raspisanie_key_added.json не найден")
        raise SystemExit("Файл raspisanie_key_added.json не найден")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла raspisanie_key_added.json: {e}")
        raise SystemExit(f"Ошибка при чтении файла raspisanie_key_added.json: {e}")

def set_sinh_time(data):
    """Устанавливает время для ключей .1 из основного урока."""
    for class_name, days in data.items():
        logging.info(f"Начинаем обработку класса: {class_name}")
        
        for day_name, lessons in days.items():
            logging.info(f"Начинаем обработку дня: {day_name}")
            
            for key, lesson in lessons.items():
                if key.endswith(".1"):
                    parent_key = key.split(".1")[0]
                    if parent_key in lessons and "time" in lessons[parent_key]:
                        lesson["time"] = lessons[parent_key]["time"]
                        logging.debug(f"Подтянуто время для ключа '{key}' из родительского урока '{parent_key}': {lesson['time']}")
    
    return data

if __name__ == "__main__":
    time.sleep(2)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'raspisanie_key_added.json')
    
    # Загрузка данных
    schedule_data = load_raspisanie(input_file_path)
    
    # Обработка данных
    updated_data = set_sinh_time(schedule_data)
    
    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_sinh_time.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)