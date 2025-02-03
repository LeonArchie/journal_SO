import csv
import json
import logging

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Открываем файл klass.csv и считываем первые значения из каждой строки (пропуская первые 3 строки)
klass = []
try:
    with open('klass.csv', 'r', encoding='windows-1251') as file:
        reader = csv.reader(file, delimiter=';')
        for i in range(3):  # Пропускаем первые 3 строки
            next(reader, None)
        for row in reader:
            if row:  # Проверяем, что строка не пустая
                klass.append(row[0].strip())
    logging.info("Файл klass.csv успешно обработан.")
except Exception as e:
    logging.error(f"Ошибка при чтении файла klass.csv: {e}")

# Открываем файл lesson.csv и считываем все строки (пропуская первые 2 строки)
lesson = []
try:
    with open('lesson.csv', 'r', encoding='windows-1251') as file:
        reader = csv.reader(file, delimiter=';')
        for i in range(2):  # Пропускаем первые 2 строки
            next(reader, None)
        for row in reader:
            if row:  # Проверяем, что строка не пустая
                lesson.append(row[0].strip())
    logging.info("Файл lesson.csv успешно обработан.")
except Exception as e:
    logging.error(f"Ошибка при чтении файла lesson.csv: {e}")

# Считываем файл raspisanie_modified.json
try:
    with open('raspisanie_modified.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    logging.info("Файл raspisanie_modified.json успешно загружен.")
except Exception as e:
    logging.error(f"Ошибка при чтении файла raspisanie_modified.json: {e}")
    exit()

# Проверяем значения в JSON файле
errors = []

for class_name, days in data.items():
    for day, lessons in days.items():
        for lesson_num, lesson_info in lessons.items():
            # Проверяем ключ "lesson"
            lesson_value = lesson_info.get("lesson", "").strip()
            if lesson_value and lesson_value not in lesson:  # Проверяем только если значение не пустое
                errors.append(f"Класс: {class_name}, День: {day}, Урок: {lesson_num}, "
                              f"Несоответствие в lesson: {lesson_value}")

            # Проверяем ключ "number"
            number_value = lesson_info.get("number", "").strip()
            if number_value and number_value not in klass:  # Проверяем только если значение не пустое
                errors.append(f"Класс: {class_name}, День: {day}, Урок: {lesson_num}, "
                              f"Несоответствие в number: {number_value}")

# Записываем ошибки в файл error.log
if errors:
    try:
        with open('error.log', 'w', encoding='utf-8') as file:
            for error in errors:
                file.write(error + '\n')
                logging.error(error)
        logging.info("Несоответствия записаны в файл error.log.")
    except Exception as e:
        logging.error(f"Ошибка при записи в файл error.log: {e}")
else:
    logging.info("Несоответствий не найдено.")