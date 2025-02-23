import csv
import json
import os
from datetime import datetime
import time

# Функция для записи логов
def log_message(log_file, level, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {level} - {message}\n"
    with open(log_file, 'a', encoding='cp1251') as f:
        f.write(log_entry)

time.sleep(2)

# Чтение файла groups.csv и формирование массива lessons
lessons = set()
try:
    with open('groups.csv', 'r', encoding='cp1251') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # Пропускаем первую строку
        for row in reader:
            if len(row) > 1:
                lessons.add(row[1])
except UnicodeDecodeError:
    print("Ошибка чтения файла groups.csv. Проверьте кодировку файла (должна быть windows-1251).")
    exit()

# Преобразуем множество в список
lessons = list(lessons)

# Чтение файла raspisanie_cab_updated.json (всегда в UTF-8)
if not os.path.exists('raspisanie_cab_updated.json'):
    print("Файл raspisanie_cab_updated.json не найден.")
    exit()

try:
    with open('raspisanie_cab_updated.json', 'r', encoding='utf-8') as jsonfile:
        schedule = json.load(jsonfile)
except json.JSONDecodeError:
    print("Ошибка декодирования JSON. Проверьте формат файла raspisanie_cab_updated.json.")
    exit()

time.sleep(2)

# Проверка данных в raspisanie_cab_updated.json
for class_name, days in schedule.items():
    for day, lessons_schedule in days.items():
        for lesson_number, lesson_data in lessons_schedule.items():
            if lesson_data['lesson'] in lessons:
                if lesson_data['groups']:
                    # Если groups не пустой, пишем в log.log
                    message = (f"Класс: {class_name}, День недели: {day}, Номер урока: {lesson_number}, "
                               f"Предмет: {lesson_data['lesson']}, Группы: {lesson_data['groups']}, Все хорошо")
                    log_message('log.log', 'INFO', message)
                else:
                    # Если groups пустой, пишем в log.log и err_groups.log
                    error_message = (f"Класс: {class_name}, День недели: {day}, Номер урока: {lesson_number}, "
                                     f"Предмет: {lesson_data['lesson']}, Группы: {lesson_data['groups']}, Ошибка: groups пустой")
                    
                    # Записываем в log.log
                    log_message('log.log', 'ERROR', error_message)
                    
                    # Записываем в chech_groups.log
                    log_message('chech_groups.log', 'ERROR', error_message)

time.sleep(2)
print("Обработка завершена. Логи записаны в файлы log.log и chech_groups.log.")