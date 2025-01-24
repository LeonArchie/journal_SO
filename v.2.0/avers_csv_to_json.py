import json
import os
import sys
from datetime import datetime

# Настройка логирования в файл
log_file = open("avers_to_json.log", "w", encoding="utf-8")

# Флаг для вывода логов в консоль
LOG_TO_CONSOLE = "--console" in sys.argv

def log_message(message, level="INFO"):
    """
    Логирует сообщение с указанным уровнем и временем.
    :param message: Сообщение для логирования.
    :param level: Уровень логирования (INFO, ERROR, DEBUG, OK и т.д.).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    # Записываем сообщение в файл
    log_file.write(log_entry + "\n")
    log_file.flush()  # Обеспечиваем запись в файл сразу

    # Если включен вывод в консоль, выводим логи туда
    if LOG_TO_CONSOLE:
        print(log_entry)

def parse_schedule(file_path, log_message):
    """
    Парсит CSV-файл с расписанием и преобразует его в JSON-структуру.
    :param file_path: Путь к CSV-файлу с расписанием.
    :param log_message: Функция логирования.
    :return: Словарь с расписанием в формате JSON.
    """
    schedule = {}  # Создаем пустой словарь для хранения расписания
    current_class = None  # Переменная для хранения текущего класса
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]  # Список дней недели
    log_message(f"Начало парсинга файла: {file_path}", "INFO")

    try:
        # Открываем CSV-файл для чтения с кодировкой UTF-8
        log_message(f"Попытка открыть файл: {file_path}", "DEBUG")
        with open(file_path, 'r', encoding='utf-8') as file:
            log_message(f"Файл {file_path} успешно открыт.", "INFO")
            lines = file.readlines()  # Читаем все строки из файла
            log_message(f"Прочитано {len(lines)} строк из файла.", "DEBUG")

            i = 0  # Индекс текущей строки
            while i < len(lines):
                line = lines[i].strip()  # Убираем лишние пробелы и символы новой строки
                log_message(f"Обработка строки {i + 1}: {line}", "DEBUG")

                # Игнорируем строки до первого вхождения "Класс -"
                if current_class is None:
                    if "Класс -" in line:
                        # Нашли строку с классом, извлекаем название класса
                        class_start = line.find("Класс -") + len("Класс -")  # Начало названия класса
                        class_end = line.find(",", class_start)  # Конец названия класса (разделитель ,)
                        if class_end == -1:
                            log_message("Не найден разделитель , после названия класса.", "ERROR")
                            return None
                        current_class = line[class_start:class_end].strip()  # Извлекаем название класса
                        schedule[current_class] = {day: {} for day in days}  # Создаем структуру для класса
                        log_message(f"Найден класс: {current_class}. Создана структура для дней недели.", "INFO")
                        log_message(f"Структура для класса {current_class}: {json.dumps(schedule[current_class], ensure_ascii=False, indent=2)}", "DEBUG")
                    i += 1
                    continue

                # Игнорируем строки с заголовками
                if line.startswith("#,Время,") or line.startswith(",,Предмет"):
                    log_message(f"Пропуск строки с заголовком: {line}", "DEBUG")
                    i += 1
                    continue

                # Обрабатываем строку с уроками
                if line:
                    parts = line.split(",")  # Разделяем строку по запятой
                    lesson_number = parts[0].strip()  # Извлекаем номер урока
                    time = parts[1].strip()  # Извлекаем время урока

                    # Если номер урока пустой, пропускаем строку
                    if not lesson_number:
                        log_message("Номер урока пустой. Пропуск строки.", "DEBUG")
                        i += 1
                        continue

                    log_message(f"Обработка урока {lesson_number} с временем {time}.", "DEBUG")

                    # Добавляем данные в каждый день недели
                    for day_index, day in enumerate(days):
                        subject_index = 2 + day_index * 2  # Индекс предмета в строке
                        room_index = 3 + day_index * 2  # Индекс кабинета в строке

                        if len(parts) > subject_index and parts[subject_index].strip():
                            # Если предмет указан, добавляем его в расписание
                            schedule[current_class][day][lesson_number] = {
                                "Время": time,
                                "Урок": parts[subject_index].strip(),
                                "Кабинет": parts[room_index].strip() if len(parts) > room_index else "",
                                "Учитель": ""  # Учитель будет добавлен позже
                            }
                            log_message(f"Добавлен урок {lesson_number} в день {day} для класса {current_class}.", "INFO")
                            log_message(f"Данные урока: {json.dumps(schedule[current_class][day][lesson_number], ensure_ascii=False, indent=2)}", "DEBUG")

                    # Обрабатываем следующую строку с учителями
                    i += 1
                    if i < len(lines):
                        teacher_parts = lines[i].strip().split(",")  # Разделяем строку с учителями
                        for day_index, day in enumerate(days):
                            teacher_index = 2 + day_index * 2  # Индекс учителя в строке
                            if len(teacher_parts) > teacher_index and teacher_parts[teacher_index].strip():
                                # Если учитель указан, добавляем его в расписание
                                schedule[current_class][day][lesson_number]["Учитель"] = teacher_parts[teacher_index].strip()
                                log_message(f"Добавлен учитель для урока {lesson_number} в день {day}: {teacher_parts[teacher_index].strip()}.", "INFO")
                                log_message(f"Обновленные данные урока: {json.dumps(schedule[current_class][day][lesson_number], ensure_ascii=False, indent=2)}", "DEBUG")
                    i += 1  # Переходим к следующей строке

                else:
                    # Если строка пустая, пропускаем её
                    log_message("Пустая строка. Пропуск.", "DEBUG")
                    i += 1

        log_message(f"Парсинг завершен. Обработано {i} строк.", "OK")  # Уровень OK для успешного завершения парсинга
        log_message(f"Результат парсинга: {json.dumps(schedule, ensure_ascii=False, indent=2)}", "DEBUG")
        return schedule

    except Exception as e:
        log_message(f"Ошибка при парсинге файла: {e}", "ERROR")
        return None

def main(file_path, log_message):
    """
    Основная функция для парсинга расписания и сохранения результата в JSON.
    :param file_path: Путь к CSV-файлу с расписанием.
    :param log_message: Функция логирования.
    :return: Возвращает True, если парсинг и сохранение прошли успешно, иначе False.
    """
    try:
        log_message(f"Начало работы скрипта avers_csv_to_json.py. Путь к файлу: {file_path}", "INFO")
        log_message("Запуск скрипта avers_csv_to_json.py...", "OK")  # Логирование запуска скрипта

        # Получаем текущую директорию, где находится скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_message(f"Текущая директория скрипта: {script_dir}", "DEBUG")

        # Парсинг расписания
        log_message("Начало парсинга расписания.", "INFO")
        parsed_schedule = parse_schedule(file_path, log_message)

        if parsed_schedule is None:
            log_message("Ошибка при парсинге расписания. Завершение работы.", "ERROR")
            return False

        # Сохранение результата в JSON-файл в UTF-8 без BOM
        output_file_path = os.path.join(script_dir, "Schedule.json")
        log_message(f"Сохранение результата в файл: {output_file_path}", "INFO")
        
        # Открываем файл с кодировкой utf-8 (без BOM)
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(parsed_schedule, json_file, ensure_ascii=False, indent=4)
        
        log_message(f"Результат успешно сохранен в файл: {output_file_path}", "OK")  # Уровень OK для успешного сохранения

        return True

    except Exception as e:
        log_message(f"Ошибка при выполнении скрипта avers_csv_to_json.py: {e}", "ERROR")
        return False

# Точка входа в программу
if __name__ == "__main__":
    # Получаем аргументы командной строки
    if len(sys.argv) < 2:
        log_message("Использование: python avers_csv_to_json.py <schedule_file> [--console]", "ERROR")
        sys.exit(1)

    # Убираем аргумент --console из списка аргументов
    schedule_file = sys.argv[1]

    # Вызов основной функции
    result = main(schedule_file, log_message)
    if result:
        log_message("Парсинг и сохранение завершены успешно.", "OK")
    else:
        log_message("Ошибка при выполнении скрипта.", "ERROR")