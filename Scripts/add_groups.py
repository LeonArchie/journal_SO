import json
import csv
import logging
import os
import time

# Настройка основного логгера
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

# Обработчик для log.log (все уровни логирования)
log_handler = logging.FileHandler('log.log', mode='w', encoding='cp1251')  # Кодировка windows-1251
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(log_handler)

# Обработчик для err_groups.log (только ERROR и выше)
error_handler = logging.FileHandler('err_groups.log', mode='w', encoding='cp1251', delay=True)  # Отложенное создание + кодировка windows-1251
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(error_handler)

# Функция для загрузки данных из groups.csv
def load_groups_csv(file_path):
    """Загружает данные из groups.csv."""
    groups_data = {}
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Пропускаем заголовки
            for row in reader:
                class_name, subject, teacher, group = row
                class_name = class_name.lower()  # Только класс переводим в нижний регистр
                key = (class_name, subject.strip(), teacher.strip())
                if key not in groups_data:
                    groups_data[key] = []
                groups_data[key].append(group.strip())  # Удаляем лишние пробелы
                logger.debug(f"Добавлена группа: {group} для ключа {key}")
        logger.info("Файл groups.csv успешно загружен")
        return groups_data
    except FileNotFoundError:
        logger.error("Файл groups.csv не найден")
        raise SystemExit("Файл groups.csv не найден")
    except UnicodeDecodeError:
        logger.error("Ошибка декодирования файла groups.csv. Проверьте кодировку файла.")
        raise SystemExit("Ошибка декодирования файла groups.csv. Проверьте кодировку файла.")

# Функция для загрузки данных из raspisanie_sinh_time.json
def load_raspisanie(file_path):
    """Загружает данные из raspisanie_sinh_time.json."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.error("Файл raspisanie_sinh_time.json не найден")
        raise SystemExit("Файл raspisanie_sinh_time.json не найден")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла raspisanie_sinh_time.json: {e}")
        raise SystemExit(f"Ошибка при чтении файла raspisanie_sinh_time.json: {e}")

# Функция для добавления групп
def add_groups(data, groups_data):
    """Добавляет группы для основных уроков и .1."""
    for class_name, days in data.items():
        class_name_lower = class_name.lower()
        logger.info(f"Начинаем обработку класса: {class_name}")
        
        for day_name, lessons in days.items():
            logger.info(f"Начинаем обработку дня: {day_name}")
            
            for key, lesson in lessons.items():
                if key.endswith(".1"):
                    # Ищем родительский ключ
                    parent_key = key.split(".1")[0]
                    
                    if parent_key not in lessons:
                        logger.warning(f"Для ключа {key} не найден родительский ключ {parent_key}. Пропускаем.")
                        continue
                    
                    # Получаем данные из родительского урока
                    parent_lesson = lessons[parent_key]
                    parent_subject = parent_lesson.get("lesson", "")
                    parent_teacher = parent_lesson.get("teach", "")
                    
                    # Проверяем, совпадают ли параметры основного и дочернего урока
                    if (
                        lesson.get("lesson") == parent_subject and
                        lesson.get("teach") == parent_teacher
                    ):
                        # Формируем ключ для поиска групп
                        key_for_groups = (class_name_lower, parent_subject.strip(), parent_teacher.strip())
                        logger.debug(f"Сформирован ключ для поиска групп (совпадающие параметры): {key_for_groups}")
                        
                        # Находим соответствующие группы
                        groups = groups_data.get(key_for_groups, [])
                        
                        if len(groups) >= 2:
                            # Распределяем группы между основным и дочерним уроками
                            parent_lesson["groups"] = groups[0]
                            lesson["groups"] = groups[1]
                            logger.info(f"Обновлены группы для ключей {parent_key} и {key}: {groups[0]}, {groups[1]}")
                        elif len(groups) == 1:
                            # Если только одна группа, присваиваем её основному уроку
                            parent_lesson["groups"] = groups[0]
                            logger.info(f"Найдена одна группа для ключа {parent_key}: {groups[0]}")
                        else:
                            # Если группы не найдены, записываем предупреждение
                            logger.error(f"Не найдено подходящих групп для ключа {key_for_groups}")
                    
                    else:
                        # Если параметры не совпадают, формируем уникальные ключи
                        parent_key_for_groups = (class_name_lower, parent_subject.strip(), parent_teacher.strip())
                        child_key_for_groups = (class_name_lower, lesson.get("lesson", "").strip(), lesson.get("teach", "").strip())
                        
                        logger.debug(f"Сформирован уникальный ключ для родительского урока: {parent_key_for_groups}")
                        logger.debug(f"Сформирован уникальный ключ для дочернего урока: {child_key_for_groups}")
                        
                        # Находим группы для каждого ключа
                        parent_groups = groups_data.get(parent_key_for_groups, [])
                        child_groups = groups_data.get(child_key_for_groups, [])
                        
                        if parent_groups:
                            parent_lesson["groups"] = parent_groups[0]
                            logger.info(f"Найдена группа для родительского урока {parent_key}: {parent_groups[0]}")
                        else:
                            logger.error(f"Не найдено подходящих групп для родительского ключа {parent_key_for_groups}")
                        
                        if child_groups:
                            lesson["groups"] = child_groups[0]
                            logger.info(f"Найдена группа для дочернего урока {key}: {child_groups[0]}")
                        else:
                            logger.error(f"Не найдено подходящих групп для дочернего ключа {child_key_for_groups}")
    
    return data

if __name__ == "__main__":
    time.sleep(2)    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    groups_file_path = os.path.join(script_dir, 'groups.csv')
    input_file_path = os.path.join(script_dir, 'raspisanie_sinh_time.json')
    
    # Загрузка данных
    groups_data = load_groups_csv(groups_file_path)
    schedule_data = load_raspisanie(input_file_path)
    
    # Обработка данных
    updated_data = add_groups(schedule_data, groups_data)
    
    # Сохранение результатов
    output_file_path = os.path.join(script_dir, 'raspisanie_groups_added.json')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)
    
    logger.info(f"Файл успешно обработан и сохранен как {output_file_path}")
    time.sleep(2)