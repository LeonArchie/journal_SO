import json
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Логирование в файл app.log
        logging.StreamHandler()  # Логирование в консоль
    ]
)

def parse_schedule(file_path):
    """
    Парсит CSV-файл с расписанием и преобразует его в JSON-структуру.
    :param file_path: Путь к CSV-файлу с расписанием.
    :return: Словарь с расписанием в формате JSON.
    """
    schedule = {}  # Создаем пустой словарь для хранения расписания
    current_class = None  # Переменная для хранения текущего класса
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]  # Список дней недели
    logging.info(f"Начало парсинга файла: {file_path}")

    # Открываем CSV-файл для чтения в кодировке cp1251
    with open(file_path, 'r', encoding='cp1251') as file:
        logging.debug(f"Файл {file_path} успешно открыт.")
        lines = file.readlines()  # Читаем все строки из файла
        logging.debug(f"Прочитано {len(lines)} строк из файла.")

    i = 0  # Индекс текущей строки
    while i < len(lines):
        line = lines[i].strip()  # Убираем лишние пробелы и символы новой строки
        logging.debug(f"Обработка строки {i + 1}: {line}")

        if line.startswith("Класс - "):
            # Нашли строку с классом, создаем новый массив для этого класса
            current_class = line.split(" - ")[1].split(";")[0].strip()  # Извлекаем название класса
            schedule[current_class] = {day: {} for day in days}  # Создаем структуру для класса
            logging.info(f"Найден класс: {current_class}. Создана структура для дней недели.")
            i += 1  # Переходим к следующей строке

        elif line.startswith("#;Время;") or line.startswith(";;Предмет"):
            # Игнорируем строки с заголовками
            logging.debug(f"Пропуск строки с заголовком: {line}")
            i += 1  # Переходим к следующей строке

        elif line:
            # Обрабатываем строку с уроками
            parts = line.split(";")  # Разделяем строку по символу ';'
            lesson_number = parts[0].strip()  # Извлекаем номер урока
            logging.debug(f"Обработка урока {lesson_number}.")

            if not lesson_number:
                # Если номер урока пустой, пропускаем строку
                logging.debug("Номер урока пустой. Пропуск строки.")
                i += 1
                continue

            # Добавляем данные в каждый день недели
            for day_index, day in enumerate(days):
                subject_index = 2 + day_index * 2  # Индекс предмета в строке
                room_index = 3 + day_index * 2  # Индекс кабинета в строке

                if len(parts) > subject_index and parts[subject_index].strip():
                    # Если предмет указан, добавляем его в расписание
                    schedule[current_class][day][lesson_number] = {
                        "Время": parts[1].strip(),  # Время урока
                        "Урок": parts[subject_index].strip(),  # Название предмета
                        "Кабинет": parts[room_index].strip(),  # Кабинет
                        "Учитель": ""  # Учитель (пока пусто)
                    }
                    logging.debug(f"Добавлен урок {lesson_number} в день {day} для класса {current_class}.")
                else:
                    logging.debug(f"Предмет для урока {lesson_number} в день {day} не указан. Пропуск.")

            # Обрабатываем следующую строку с учителями
            i += 1
            if i < len(lines):
                teacher_parts = lines[i].strip().split(";")  # Разделяем строку с учителями
                for day_index, day in enumerate(days):
                    teacher_index = 2 + day_index * 2  # Индекс учителя в строке
                    if len(teacher_parts) > teacher_index and teacher_parts[teacher_index].strip():
                        # Если учитель указан, добавляем его в расписание
                        schedule[current_class][day][lesson_number]["Учитель"] = teacher_parts[teacher_index].strip()
                        logging.debug(f"Добавлен учитель для урока {lesson_number} в день {day}: {teacher_parts[teacher_index].strip()}.")
                    else:
                        logging.debug(f"Учитель для урока {lesson_number} в день {day} не указан.")
            i += 1  # Переходим к следующей строке

        else:
            # Если строка пустая, пропускаем её
            logging.debug("Пустая строка. Пропуск.")
            i += 1

    logging.info(f"Парсинг завершен. Обработано {i} строк.")
    logging.debug(f"Результат парсинга: {json.dumps(schedule, ensure_ascii=False, indent=2)}")
    return schedule

# Путь к файлу
file_path = '/home/archie/EDU/rasp.csv'
logging.info(f"Начало работы скрипта. Путь к файлу: {file_path}")

# Парсинг расписания
logging.info("Начало парсинга расписания.")
parsed_schedule = parse_schedule(file_path)

# Вывод результата в консоль
logging.info("Результат парсинга:")
logging.info(json.dumps(parsed_schedule, ensure_ascii=False, indent=4))

# Сохранение результата в JSON-файл
output_file_path = '/home/archie/EDU/schedule.json'
logging.info(f"Сохранение результата в файл: {output_file_path}")
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(parsed_schedule, json_file, ensure_ascii=False, indent=4)

logging.info(f"Результат успешно сохранен в файл: {output_file_path}")
logging.info("Работа скрипта завершена.")