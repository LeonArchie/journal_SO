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
    if not os.path.exists(input_file):
        logging.error(f"Файл {input_file} не найден.")
        print(f"Ошибка: Файл {input_file} не найден.")
        return
    
    logging.info(f"Начало обработки файла {input_file}.")
    
    result = {}
    current_class = None
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    started_processing = False  # Флаг для начала обработки
    last_lesson_number = {}  # Словарь для хранения последних номеров уроков для каждого дня
    
    try:
        with open(input_file, 'r', encoding='windows-1251') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            for row in reader:
                logging.debug(f"Обработка строки: {row}")
                
                # Пропускаем строки до первой строки "Класс -"
                if not started_processing:
                    if row and row[0].startswith("Класс - "):
                        started_processing = True  # Начинаем обработку
                    else:
                        continue
                
                if not row or all(not cell.strip() for cell in row):  # Пропускаем пустые строки
                    continue
                
                # Ищем строку с названием класса
                if row[0].startswith("Класс - "):
                    current_class = row[0].replace("Класс - ", "").replace(";;;;;;;;;;", "")
                    result[current_class] = {day: {} for day in days}
                    logging.info(f"Обработка класса: {current_class}")
                    last_lesson_number = {day: None for day in days}  # Сбрасываем счетчик уроков
                    continue
                
                # Пропускаем строки начинающиеся с '#'
                if row[0].startswith("#") or (row[0] and row[0].strip() == ""):
                    continue
                
                # Обработка строки с временем и уроками
                if len(row) >= 12 and row[0].isdigit():
                    lesson_number = row[0]
                    times = row[1]
                    
                    for i, day in enumerate(days):
                        lesson_info = {
                            "time": times,
                            "lesson": row[2 + 2 * i].strip(),
                            "teach": "",
                            "number": row[3 + 2 * i].strip()
                        }
                        
                        # Если уже есть запись с таким номером урока, добавляем ".1"
                        if lesson_number in result[current_class][day]:
                            lesson_number += ".1"
                        
                        result[current_class][day][lesson_number] = lesson_info
                        last_lesson_number[day] = lesson_number  # Сохраняем последний номер урока
                    
                    continue
                
                # Обработка строки с преподавателями
                if len(row) >= 12 and not row[0].isdigit():
                    for i, day in enumerate(days):
                        teacher = row[2 + 2 * i].strip()
                        if teacher and last_lesson_number[day]:  # Проверяем, что учитель указан и есть номер урока
                            result[current_class][day][last_lesson_number[day]]["teach"] = teacher
                    
                    continue
                
                # Обработка строк, начинающихся с ';;' (добавление '.1')
                if row[0].startswith(";;"):
                    for i, day in enumerate(days):
                        if last_lesson_number[day]:
                            new_lesson_number = f"{last_lesson_number[day].split('.')[0]}.1"
                            if new_lesson_number in result[current_class][day]:
                                new_lesson_number += ".1"
                            
                            # Копируем данные из предыдущего урока
                            previous_lesson = result[current_class][day][last_lesson_number[day]]
                            result[current_class][day][new_lesson_number] = {
                                "time": previous_lesson["time"],
                                "lesson": row[2 + 2 * i].strip(),
                                "teach": "",
                                "number": row[3 + 2 * i].strip()
                            }
                            last_lesson_number[day] = new_lesson_number  # Обновляем последний номер урока
                    
                    continue
        
        # Записываем результат в JSON файл
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False, indent=4)
        
        logging.info(f"Успешно завершена обработка файла {input_file}. Результат сохранен в {output_file}.")
    
    except Exception as e:
        logging.error(f"Ошибка при обработке файла {input_file}: {str(e)}")
        print(f"Ошибка: {str(e)}")

# Вызов функции
if __name__ == "__main__":
    input_filename = 'raspisanie.csv'
    output_filename = 'raspisanie.json'
    convert_csv_to_json(input_filename, output_filename)