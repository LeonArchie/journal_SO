import json
import logging
import os
from collections import OrderedDict
import time

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_raspisanie(file_path):
    """Загружает данные из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logging.info(f"Файл успешно загружен: {file_path}")
        return data
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
        raise SystemExit(f"Файл не найден: {file_path}")
    except Exception as e:
        logging.error(f"Ошибка при чтении файла {file_path}: {e}")
        raise SystemExit(f"Ошибка при чтении файла {file_path}: {e}")

def add_missing_keys(data):
    """Добавляет отсутствующие основные и дополнительные ключи с подробным логированием."""
    empty_template = {
        "time": "",
        "lesson": "",
        "teach": "",
        "number": "",
        "groups": ""
    }

    for class_name, days in data.items():
        logging.info(f"=== Начинается обработка класса: {class_name} ===")

        # Собираем все уникальные основные и дополнительные ключи
        all_main_keys = set()
        all_dot_one_keys = {}  # Словарь для хранения дополнительных ключей по основным

        for day_name, lessons in days.items():
            logging.debug(f"Сбор ключей из дня: {day_name}")
            for key in lessons:
                if key.isdigit():  # Основные ключи
                    all_main_keys.add(key)
                elif key.endswith(".1"):  # Дополнительные ключи
                    base_key = key.split(".")[0]
                    if base_key not in all_dot_one_keys:
                        all_dot_one_keys[base_key] = set()
                    all_dot_one_keys[base_key].add(key)

        # Логируем собранные ключи
        logging.info(f"Все основные ключи для класса {class_name}: {sorted(all_main_keys, key=int)}")
        logging.info(f"Все дополнительные ключи для класса {class_name}: {all_dot_one_keys}")

        # Проверяем каждый день на наличие основных и дополнительных ключей
        for day_name, lessons in days.items():
            existing_keys = set(lessons.keys())
            ordered_lessons = OrderedDict(sorted(lessons.items(), key=lambda x: int(x[0].split('.')[0])))
            logging.info(f"Обработка дня: {day_name}. Существующие ключи: {sorted(existing_keys)}")

            # Шаг 1: Добавляем отсутствующие основные ключи
            added_main_keys = []
            for main_key in sorted(all_main_keys, key=int):
                if main_key not in existing_keys:
                    ordered_lessons[main_key] = empty_template.copy()
                    added_main_keys.append(main_key)
                    logging.info(f"Добавлен основной ключ {main_key} в день {day_name}")

            if added_main_keys:
                logging.info(f"В день {day_name} добавлены основные ключи: {added_main_keys}")
            else:
                logging.info(f"В день {day_name} все основные ключи уже существуют.")

            # Шаг 2: Добавляем отсутствующие дополнительные ключи
            added_dot_one_keys = []
            for base_key, dot_one_keys in all_dot_one_keys.items():
                if base_key in existing_keys or base_key in added_main_keys:  # Проверяем, существует ли основной ключ
                    for dot_one_key in sorted(dot_one_keys):
                        if dot_one_key not in existing_keys:
                            ordered_lessons[dot_one_key] = empty_template.copy()
                            added_dot_one_keys.append(dot_one_key)
                            logging.info(f"Добавлен дополнительный ключ {dot_one_key} в день {day_name}")

            if added_dot_one_keys:
                logging.info(f"В день {day_name} добавлены дополнительные ключи: {added_dot_one_keys}")
            else:
                logging.info(f"В день {day_name} все дополнительные ключи уже существуют.")

            # Обновляем данные для текущего дня
            days[day_name] = ordered_lessons
            logging.info(f"День {day_name} успешно обработан. Итоговые ключи: {list(ordered_lessons.keys())}")

        logging.info(f"=== Обработка класса {class_name} завершена ===")

    return data


if __name__ == "__main__":
    time.sleep(2)  # Задержка перед началом работы
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'raspisanie_groups_added.json')

    # Загрузка данных
    schedule_data = load_raspisanie(input_file_path)

    # Обработка данных
    updated_data = add_missing_keys(schedule_data)

    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_null_lesson_added.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)

    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)  # Финальная задержка перед завершением