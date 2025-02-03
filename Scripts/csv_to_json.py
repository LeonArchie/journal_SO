import csv
import json
import logging
import os

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def convert_csv_to_json(input_file, output_file):
    """
    Основная функция для конвертации CSV файла с расписанием в JSON.
    """
    if not os.path.exists(input_file):
        logging.error(f"Файл {input_file} не найден.")
        print(f"Ошибка: Файл {input_file} не найден.")
        return
    
    logging.info(f"Начало обработки файла {input_file}.")
    
    result = {}  # Результирующий словарь для хранения данных
    current_class = None  # Текущий класс, который обрабатывается
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]  # Дни недели
    previous_lesson_number = None  # Переменная для отслеживания последнего основного номера урока
    
    try:
        with open(input_file, 'r', encoding='windows-1251') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            rows = list(reader)  # Читаем все строки
            logging.info(f"Файл {input_file} успешно прочитан. Всего строк: {len(rows)}.")
            
            i = 0
            # Игнорируем все строки до первого вхождения "Класс - "
            while i < len(rows):
                row = rows[i]
                logging.debug(f"Обработка строки {i + 1}: {row}")
                
                if row and row[0].startswith("Класс - "):
                    logging.debug(f"Найдено начало расписания для класса: {row[0]}.")
                    break
                i += 1
            
            # Основной цикл обработки расписания
            while i < len(rows):
                row = rows[i]
                logging.debug(f"Обработка строки {i + 1}: {row}")
                
                # Обработка строки с названием класса
                if row and row[0].startswith("Класс - "):
                    # Удаляем подстроку "Класс - " и ";;;;;;;;;;"
                    class_name = row[0].replace("Класс - ", "").replace(";;;;;;;;;;", "").strip()
                    result[class_name] = {day: {} for day in days}  # Создаем структуру для класса
                    current_class = class_name
                    logging.info(f"Начата обработка класса: {current_class}.")
                    previous_lesson_number = None  # Сбрасываем предыдущий номер урока
                    i += 4  # Пропускаем заголовочные строки
                    continue
                
                # Обработка пар строк (урок и учитель)
                if i + 1 < len(rows):
                    par_lesson = rows[i]  # Строка с уроком
                    teach_lesson = rows[i + 1]  # Строка с учителем
                    logging.debug(f"Обработка пары строк: урок = {par_lesson}, учитель = {teach_lesson}.")
                    
                    # Проверка на дополнительный урок
                    if par_lesson and not par_lesson[0].strip():
                        logging.debug("Обнаружен дополнительный урок.")
                        process_lesson(par_lesson, teach_lesson, result[current_class], days, is_additional=True, previous_lesson_number=previous_lesson_number)
                        i += 2
                    else:
                        # Основной урок
                        logging.debug("Обработка основного урока.")
                        process_lesson(par_lesson, teach_lesson, result[current_class], days)
                        previous_lesson_number = par_lesson[0].strip() if par_lesson[0].strip() else previous_lesson_number
                        i += 2
                
                # Проверка на пустую строку (конец расписания для текущего класса)
                if i < len(rows) and (not rows[i] or all(not cell.strip() for cell in rows[i])):
                    logging.debug(f"Пустая строка {i + 1}. Ожидание нового класса.")
                    current_class = None
                    i += 1
        
        # Запись результата в JSON файл
        logging.info(f"Запись результата в файл {output_file}.")
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False, indent=4)
        
        logging.info(f"Успешно завершена обработка файла {input_file}. Результат сохранен в {output_file}.")
    
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {input_file}: {str(e)}")
        print(f"Ошибка: {str(e)}")

def process_lesson(par_lesson, teach_lesson, class_data, days, is_additional=False, previous_lesson_number=None):
    """
    Обрабатывает урок и добавляет его в структуру класса.
    :param par_lesson: Строка с данными урока.
    :param teach_lesson: Строка с данными учителя.
    :param class_data: Структура данных класса.
    :param days: Список дней недели.
    :param is_additional: Флаг, указывающий, является ли урок дополнительным.
    :param previous_lesson_number: Номер предыдущего основного урока.
    """
    if not par_lesson or not teach_lesson:
        logging.warning("Пустые данные урока. Пропускаем.")
        return
    
    # Извлекаем номер урока (для основного урока)
    lesson_number = par_lesson[0].strip() if par_lesson[0] else ""
    logging.debug(f"Номер урока: {lesson_number}.")
    
    # Если это дополнительный урок, используем previous_lesson_number
    if is_additional and previous_lesson_number:
        lesson_key = f"{previous_lesson_number}.1"
    elif is_additional:
        logging.error("Недостаточно данных для формирования ключа дополнительного урока.")
        return
    else:
        lesson_key = lesson_number
    
    # Извлекаем время урока (оно одинаковое для основного и дополнительного)
    lesson_time = par_lesson[1].strip() if len(par_lesson) > 1 else ""
    logging.debug(f"Время урока: {lesson_time}.")
    
    # Обрабатываем каждый день недели
    for day_idx, day in enumerate(days):
        # Проверяем длину строк для избежания ошибок индексации
        if len(par_lesson) < (2 + 2 * day_idx + 1) or len(teach_lesson) < (2 + 2 * day_idx + 1):
            logging.warning(f"Недостаточно данных для дня {day}. Пропускаем.")
            continue
        
        # Извлекаем данные урока для текущего дня
        lesson_name = par_lesson[2 + 2 * day_idx].strip()  # Название урока
        lesson_room = par_lesson[3 + 2 * day_idx].strip()  # Кабинет
        teacher_name = teach_lesson[2 + 2 * day_idx].strip()  # Учитель
        
        # Пропускаем пустые уроки
        if not lesson_name:
            logging.debug(f"Урок в {day} отсутствует. Пропускаем.")
            continue
        
        # Добавляем урок в структуру
        logging.debug(f"Добавление урока с ключом {lesson_key} в {day}.")
        class_data[day][lesson_key] = {
            "time": lesson_time,
            "lesson": lesson_name,
            "teach": teacher_name,
            "number": lesson_room
        }

# Вызов функции
if __name__ == "__main__":
    input_filename = 'raspisanie.csv'
    output_filename = 'raspisanie.json'
    convert_csv_to_json(input_filename, output_filename)