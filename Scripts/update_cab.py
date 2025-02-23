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
    """Загружает данные из raspisanie_sorted_schedule.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.error("Файл raspisanie_sorted_schedule.json не найден")
        raise SystemExit("Файл raspisanie_sorted_schedule.json не найден")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла raspisanie_sorted_schedule.json: {e}")
        raise SystemExit(f"Ошибка при чтении файла raspisanie_sorted_schedule.json: {e}")

def update_dot_one_fields(data):
    """Обновляет поля в массивах .1."""
    for class_name, days in data.items():
        logging.info(f"Обновление полей в .1 для класса: {class_name}")
        
        for day_name, lessons in days.items():
            for key, lesson in lessons.items():
                if key.endswith(".1"):
                    if all(lesson.get(field) for field in ["time", "lesson", "teach"]) and not lesson.get("number"):
                        lesson["number"] = "Нет кабинета"
                        logging.info(f"Установлено значение 'Нет кабинета' для ключа {key}")
    
    return data

if __name__ == "__main__":
    time.sleep(2)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'raspisanie_sorted_schedule.json')
    
    # Загрузка данных
    schedule_data = load_raspisanie(input_file_path)
    
    # Обработка данных
    updated_data = update_dot_one_fields(schedule_data)
    
    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_cab_updated.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)