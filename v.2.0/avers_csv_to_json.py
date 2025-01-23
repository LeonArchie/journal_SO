import json
import os
import sys
from datetime import datetime

def log_message(message, level):
    """
    Логирует сообщение с указанным уровнем и временем.
    Эта функция будет передана из journal_SO.py.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Получаем текущее время
    log_entry = f"[{timestamp}] [{level}] {message}"  # Добавляем время в лог
    print(log_entry)  # Временный вывод в консоль для отладки

def parse_schedule(file_path, log_message):
    """
    Парсит CSV-файл с расписанием и преобразует его в JSON-структуру.
    :param file_path: Путь к CSV-файлу с расписанием.
    :param log_message: Функция логирования.
    :return: Словарь с расписанием в формате JSON.
    """
    schedule = {}  # Создаем пустой словарь для хранения расписания
    current_class = None  # Переменная для хранения текущего класса
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]  # Список дней недели
    log_message(f"Начало парсинга файла: {file_path}", "INFO")

    # Открываем CSV-файл для чтения в кодировке cp1251
    with open(file_path, 'r', encoding='cp1251') as file:
        log_message(f"Файл {file_path} успешно открыт.", "DEBUG")
        lines = file.readlines()  # Читаем все строки из файла
        log_message(f"Прочитано {len(lines)} строк из файла.", "DEBUG")

    i = 0  # Индекс текущей строки
    while i < len(lines):
        line = lines[i].strip()  # Убираем лишние пробелы и символы новой строки
        log_message(f"Обработка строки {i + 1}: {line}", "DEBUG")

        if line.startswith("Класс - "):
            # Нашли строку с классом, создаем новый массив для этого класса
            current_class = line.split(" - ")[1].split(";")[0].strip()  # Извлекаем название класса
            schedule[current_class] = {day: {} for day in days}  # Создаем структуру для класса
            log_message(f"Найден класс: {current_class}. Создана структура для дней недели.", "INFO")
            i += 1  # Переходим к следующей строке

        elif line.startswith("#;Время;") or line.startswith(";;Предмет"):
            # Игнорируем строки с заголовками
            log_message(f"Пропуск строки с заголовком: {line}", "DEBUG")
            i += 1  # Переходим к следующей строке

        elif line:
            # Обрабатываем строку с уроками
            parts = line.split(";")  # Разделяем строку по символу ';'
            lesson_number = parts[0].strip()  # Извлекаем номер урока
            log_message(f"Обработка урока {lesson_number}.", "DEBUG")

            if not lesson_number:
                # Если номер урока пустой, пропускаем строку
                log_message("Номер урока пустой. Пропуск строки.", "DEBUG")
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
                    log_message(f"Добавлен урок {lesson_number} в день {day} для класса {current_class}.", "DEBUG")
                else:
                    log_message(f"Предмет для урока {lesson_number} в день {day} не указан. Пропуск.", "DEBUG")

            # Обрабатываем следующую строку с учителями
            i += 1
            if i < len(lines):
                teacher_parts = lines[i].strip().split(";")  # Разделяем строку с учителями
                for day_index, day in enumerate(days):
                    teacher_index = 2 + day_index * 2  # Индекс учителя в строке
                    if len(teacher_parts) > teacher_index and teacher_parts[teacher_index].strip():
                        # Если учитель указан, добавляем его в расписание
                        schedule[current_class][day][lesson_number]["Учитель"] = teacher_parts[teacher_index].strip()
                        log_message(f"Добавлен учитель для урока {lesson_number} в день {day}: {teacher_parts[teacher_index].strip()}.", "DEBUG")
                    else:
                        log_message(f"Учитель для урока {lesson_number} в день {day} не указан.", "DEBUG")
            i += 1  # Переходим к следующей строке

        else:
            # Если строка пустая, пропускаем её
            log_message("Пустая строка. Пропуск.", "DEBUG")
            i += 1

    log_message(f"Парсинг завершен. Обработано {i} строк.", "INFO")
    log_message(f"Результат парсинга: {json.dumps(schedule, ensure_ascii=False, indent=2)}", "DEBUG")
    return schedule

def main(file_path, log_message):
    """
    Основная функция для парсинга расписания и сохранения результата в JSON.
    :param file_path: Путь к CSV-файлу с расписанием.
    :param log_message: Функция логирования.
    :return: Возвращает True, если парсинг и сохранение прошли успешно, иначе False.
    """
    try:
        log_message(f"Начало работы скрипта avers_csv_to_json.py. Путь к файлу: {file_path}", "INFO")

        # Получаем текущую директорию, где находится скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_message(f"Текущая директория скрипта: {script_dir}", "DEBUG")

        # Парсинг расписания
        log_message("Начало парсинга расписания.", "INFO")
        parsed_schedule = parse_schedule(file_path, log_message)

        # Сохранение результата в JSON-файл
        output_file_path = os.path.join(script_dir, "Schedule.json")
        log_message(f"Сохранение результата в файл: {output_file_path}", "INFO")
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(parsed_schedule, json_file, ensure_ascii=False, indent=4)
        log_message(f"Результат успешно сохранен в файл: {output_file_path}", "INFO")

        return True

    except Exception as e:
        log_message(f"Ошибка при выполнении скрипта avers_csv_to_json.py: {e}", "ERROR")
        return False

if __name__ == "__main__":
    # Пример вызова скрипта напрямую (для тестирования)
    def log_message(message, level):
        print(f"[{level}] {message}")

    # Получаем аргументы командной строки
    if len(sys.argv) != 2:
        print("Использование: python avers_csv_to_json.py <schedule_file>")
        sys.exit(1)

    schedule_file = sys.argv[1]

    # Вызов основной функции
    result = main(schedule_file, log_message)
    if result:
        print("Парсинг и сохранение завершены успешно.")
    else:
        print("Ошибка при выполнении скрипта.")