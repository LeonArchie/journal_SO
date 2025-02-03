import json
import os
import logging
from collections import OrderedDict

# Настройка логирования
logging.basicConfig(
    filename='log.log',  # Файл для записи логов
    level=logging.DEBUG,  # Уровень детализации логов
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи логов
)

def rename_keys_and_update_time(data):
    for class_name, days in data.items():
        logging.info(f"Обработка класса: {class_name}")
        for day_name, lessons in days.items():
            logging.info(f"Обработка дня: {day_name}")
            # Создаем новый упорядоченный словарь для временного хранения измененных данных
            new_lessons = OrderedDict()
            previous_key = None
            keys = list(lessons.keys())
            
            for key in keys:
                if key == ".1" and previous_key is not None:
                    # Переименовываем .1 в <previous_key>.1 и добавляем в новый словарь
                    new_key = f"{previous_key}.1"
                    logging.debug(f"Переименование ключа '.1' в '{new_key}'")
                    new_lessons[new_key] = lessons[key]
                    # Подтягиваем время из основного урока
                    if previous_key in lessons and "time" in lessons[previous_key]:
                        new_lessons[new_key]["time"] = lessons[previous_key]["time"]
                        logging.debug(f"Подтянуто время для ключа '{new_key}': {lessons[previous_key]['time']}")
                    else:
                        logging.warning(f"Не удалось подтянуть время для ключа '{new_key}', так как предыдущий ключ отсутствует или не содержит поля 'time'")
                else:
                    # Копируем остальные ключи без изменений
                    new_lessons[key] = lessons[key]
                    if key.isdigit():  # Обновляем previous_key только если это числовой ключ
                        previous_key = key
                        logging.debug(f"Обновление previous_key на '{key}'")
                    else:
                        previous_key = None  # Сбрасываем previous_key для нечисловых ключей
            
            # Заменяем старый словарь новым
            days[day_name] = new_lessons
            logging.info(f"Обновленные данные для дня {day_name}: {new_lessons}")

    return data


def add_dot_one_to_all_days(data):
    for class_name, days in data.items():
        logging.info(f"Добавление .1 в все дни для класса: {class_name}")
        
        # Найдем все уникальные ключи вида X.1
        dot_one_keys = set()
        for day_name, lessons in days.items():
            for key in lessons:
                if key.endswith(".1"):
                    dot_one_keys.add(key)
                    logging.debug(f"Найден ключ .1 в дне {day_name}: {key}")
        
        # Если есть ключи .1, добавим их в остальные дни
        if dot_one_keys:
            empty_dot_one_template = {
                "time": "",
                "lesson": "",
                "teach": "",
                "number": ""
            }
            for day_name, lessons in days.items():
                existing_keys = set(lessons.keys())
                
                # Создаем новый упорядоченный словарь для текущего дня
                ordered_lessons = OrderedDict()
                lesson_list = list(lessons.items())  # Получаем список пар (ключ, значение)
                i = 0
                
                while i < len(lesson_list):
                    key, value = lesson_list[i]
                    
                    # Добавляем текущий ключ в упорядоченный словарь
                    ordered_lessons[key] = value
                    
                    # Проверяем, нужно ли добавить соответствующий .1 после текущего ключа
                    if key.isdigit() and f"{key}.1" in dot_one_keys and f"{key}.1" not in existing_keys:
                        dot_one_key = f"{key}.1"
                        ordered_lessons[dot_one_key] = empty_dot_one_template.copy()
                        logging.info(f"Добавлен пустой массив {dot_one_key} в день {day_name} после ключа {key}")
                    
                    i += 1
                
                # Заменяем старый словарь упорядоченным
                days[day_name] = ordered_lessons
    
    return data


# Определение пути к файлу относительно расположения скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к папке со скриптом

# Чтение файла raspisanie.json
input_file_path = os.path.join(script_dir, 'raspisanie.json')
output_file_path = os.path.join(script_dir, 'raspisanie_modified.json')

try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        schedule_data = json.load(file, object_pairs_hook=OrderedDict)
    logging.info("Файл raspisanie.json успешно загружен")
except FileNotFoundError:
    logging.error("Файл raspisanie.json не найден")
    raise SystemExit("Файл raspisanie.json не найден")

# Переименование ключей и обновление времени
schedule_data = rename_keys_and_update_time(schedule_data)

# Добавление .1 в остальные дни недели
schedule_data = add_dot_one_to_all_days(schedule_data)

# Запись измененного JSON обратно в файл
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(schedule_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
except Exception as e:
    logging.error(f"Ошибка при записи файла: {e}")
    raise SystemExit(f"Ошибка при записи файла: {e}")