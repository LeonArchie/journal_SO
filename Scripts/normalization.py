import json
import os
import csv
import logging
from collections import OrderedDict

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_groups_csv(file_path):
    """Загружает данные из groups.csv и создает словарь для быстрого поиска."""
    groups_data = {}
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Пропускаем заголовок
            for row in reader:
                class_name, subject, teacher, group = row
                class_name = class_name.lower()  # Только класс переводим в нижний регистр
                key = (class_name, subject.strip(), teacher.strip())
                if key not in groups_data:
                    groups_data[key] = []
                groups_data[key].append(group.strip())  # Удаляем лишние пробелы
                logging.debug(f"Добавлена группа: {group} для ключа {key}")
        logging.info("Файл groups.csv успешно загружен")
        return groups_data
    except FileNotFoundError:
        logging.error("Файл groups.csv не найден")
        raise SystemExit("Файл groups.csv не найден")
    except UnicodeDecodeError:
        logging.error("Ошибка декодирования файла groups.csv. Проверьте кодировку файла.")
        raise SystemExit("Ошибка декодирования файла groups.csv. Проверьте кодировку файла.")

def process_raspisanie(data, groups_data):
    """Обрабатывает данные из raspisanie.json согласно новой логике."""
    for class_name, days in data.items():
        class_name_lower = class_name.lower()
        logging.info(f"Начинаем обработку класса: {class_name}")
        
        for day_name, lessons in days.items():
            logging.info(f"Начинаем обработку дня: {day_name}")
            
            new_lessons = OrderedDict()
            previous_key = None
            
            for key, lesson in lessons.items():
                logging.debug(f"Обработка урока с ключом: {key}")
                
                if key.endswith(".1") and previous_key is not None:
                    # Обработка *.1
                    parent_key = previous_key
                    parent_lesson = lessons.get(parent_key, {})
                    
                    if "time" in parent_lesson:
                        lesson["time"] = parent_lesson["time"]
                        logging.debug(f"Подтянуто время для ключа '{key}' из родительского урока '{parent_key}': {parent_lesson['time']}")
                    
                    # Проверяем наличие lesson и teach в основном уроке
                    if "lesson" in parent_lesson and "teach" in parent_lesson:
                        subject = parent_lesson["lesson"]  # Без изменения регистра
                        teacher = parent_lesson["teach"]  # Сохраняем пробелы
                        
                        # Делаем выборку из groups.csv
                        key_for_groups = (class_name_lower, subject, teacher)
                        groups = groups_data.get(key_for_groups, [])
                        logging.debug(f"Поиск групп для ключа {key_for_groups}. Найдено групп: {len(groups)}")
                        
                        if len(groups) == 2:
                            # Проверяем, совпадают ли параметры в *.1
                            if all(k in lesson for k in ["lesson", "teach"]) and \
                               lesson["lesson"] == parent_lesson["lesson"] and \
                               lesson["teach"] == parent_lesson["teach"]:
                                # Записываем группы
                                parent_lesson["groups"] = groups[0]
                                lesson["groups"] = groups[1]
                                logging.info(f"Обновлены группы для ключей {parent_key} и {key}: {groups[0]}, {groups[1]}")
                            else:
                                # Оставляем только первую группу
                                parent_lesson["groups"] = groups[0]
                                logging.warning(f"Параметры в {key} не совпадают, оставлено первое значение группы: {groups[0]}")
                        elif len(groups) == 1:
                            # Оставляем только первую группу
                            parent_lesson["groups"] = groups[0]
                            logging.info(f"Найдена одна группа для ключа {parent_key}: {groups[0]}")
                        else:
                            logging.warning(f"Не найдено подходящих групп для ключа {parent_key}")
                    
                    # Добавляем *.1 в новый словарь
                    new_lessons[key] = lesson
                
                else:
                    # Добавляем остальные ключи без изменений
                    new_lessons[key] = lesson
                    if key.isdigit():
                        previous_key = key
                        logging.debug(f"Обновление previous_key на '{key}'")
                    else:
                        previous_key = None
                        logging.debug(f"Сброс previous_key для нечислового ключа '{key}'")
            
            # Заменяем старый словарь новым
            days[day_name] = new_lessons
            logging.info(f"Обновленные данные для дня {day_name}: {new_lessons}")
    
    return data

def add_dot_one_to_all_days(data):
    """Добавляет .1 в остальные дни недели для каждого класса."""
    for class_name, days in data.items():
        logging.info(f"Добавление .1 в все дни для класса: {class_name}")
        
        dot_one_keys = set()
        for day_name, lessons in days.items():
            for key in lessons:
                if key.endswith(".1"):
                    dot_one_keys.add(key)
                    logging.debug(f"Найден ключ .1 в день {day_name}: {key}")
        
        if dot_one_keys:
            empty_dot_one_template = {
                "time": "",
                "lesson": "",
                "teach": "",
                "number": "",
                "groups": ""
            }
            for day_name, lessons in days.items():
                existing_keys = set(lessons.keys())
                ordered_lessons = OrderedDict(lessons.items())
                i = 0
                
                while i < len(ordered_lessons):
                    key, value = list(ordered_lessons.items())[i]
                    
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

def update_dot_one_fields(data):
    """Обновляет поля в массивах *.1 и переставляет их в правильный порядок."""
    for class_name, days in data.items():
        logging.info(f"Обновление полей в *.1 для класса: {class_name}")
        
        for day_name, lessons in days.items():
            logging.info(f"Обработка дня: {day_name}")
            
            # Создаем временный упорядоченный словарь для нового порядка
            new_lessons = OrderedDict()
            
            for key in sorted(lessons, key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else x):
                lesson = lessons[key]
                
                if key.endswith(".1"):
                    # Проверяем условия для обновления поля number
                    if all(lesson.get(field) for field in ["time", "lesson", "teach"]) and not lesson.get("number"):
                        lesson["number"] = "Нет кабинета"
                        logging.info(f"Установлено значение 'Нет кабинета' для ключа {key}")
                
                # Добавляем урок в новый словарь
                new_lessons[key] = lesson
            
            # Заменяем старый словарь новым
            days[day_name] = new_lessons
            logging.info(f"Обновленные данные для дня {day_name}: {new_lessons}")
    
    return data

# Определение путей к файлам
script_dir = os.path.dirname(os.path.abspath(__file__))
groups_file_path = os.path.join(script_dir, 'groups.csv')
input_file_path = os.path.join(script_dir, 'raspisanie.json')
output_file_path = os.path.join(script_dir, 'raspisanie_modified.json')

# Чтение файла groups.csv
try:
    groups_data = load_groups_csv(groups_file_path)
except Exception as e:
    logging.error(f"Ошибка при чтении файла groups.csv: {e}")
    raise SystemExit(f"Ошибка при чтении файла groups.csv: {e}")

# Чтение файла raspisanie.json
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        schedule_data = json.load(file, object_pairs_hook=OrderedDict)
    
    # Преобразуем названия классов в нижний регистр
    normalized_schedule_data = OrderedDict()
    for class_name, days in schedule_data.items():
        normalized_class_name = class_name.lower()
        normalized_schedule_data[normalized_class_name] = days
        logging.debug(f"Преобразование класса '{class_name}' в нижний регистр: '{normalized_class_name}'")
    
    schedule_data = normalized_schedule_data  # Используем нормализованные данные
    logging.info("Файл raspisanie.json успешно загружен и нормализован")
except FileNotFoundError:
    logging.error("Файл raspisanie.json не найден")
    raise SystemExit("Файл raspisanie.json не найден")
except Exception as e:
    logging.error(f"Ошибка при чтении файла raspisanie.json: {e}")
    raise SystemExit(f"Ошибка при чтении файла raspisanie.json: {e}")

# Обработка данных
try:
    schedule_data = process_raspisanie(schedule_data, groups_data)
    schedule_data = add_dot_one_to_all_days(schedule_data)
    schedule_data = update_dot_one_fields(schedule_data)  # Вызываем новую функцию
    logging.info("Данные успешно обработаны")
except Exception as e:
    logging.error(f"Ошибка при обработке данных: {e}")
    raise SystemExit(f"Ошибка при обработке данных: {e}")

# Запись измененного JSON обратно в файл
try:
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(schedule_data, file, ensure_ascii=False, indent=4)
    logging.info(f"Файл успешно обработан и сохранен как {output_file_path}")
except Exception as e:
    logging.error(f"Ошибка при записи файла: {e}")
    raise SystemExit(f"Ошибка при записи файла: {e}")