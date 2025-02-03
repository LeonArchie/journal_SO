import json
import csv
import logging

# Настройка логирования
logging.basicConfig(filename='log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def create_csv_schedule(json_file_path, output_csv_path):
    """
    Преобразует JSON-файл с расписанием в CSV-файл.
    """
    logging.info("Начало работы функции create_csv_schedule.")
    logging.info(f"Загрузка JSON-файла с расписанием: {json_file_path}")
    
    # Загружаем JSON-файл с расписанием
    with open(json_file_path, 'r', encoding='utf-8') as file:
        schedule = json.load(file)
    logging.info("JSON-файл успешно загружен.")
    
    # Создаем CSV-файл в кодировке Windows-1251
    logging.info(f"Создание CSV-файла: {output_csv_path}")
    with open(output_csv_path, 'w', encoding='windows-1251', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')  # Используем ';' как разделитель
        
        # Проходим по каждому классу в JSON
        for class_name, days in schedule.items():
            logging.info(f"Обработка класса: {class_name}")
            
            # Записываем заголовок класса
            writer.writerow([f"Класс: {class_name}"])
            writer.writerow([])  # Пустая строка для читаемости
            logging.debug(f"Заголовок класса '{class_name}' записан в CSV.")
            
            # Записываем заголовки дней недели
            writer.writerow(["", "", "Пн", "Вт", "Ср", "Чт", "Пт"])
            writer.writerow([])  # Пустая строка
            logging.debug("Заголовки дней недели записаны в CSV.")
            
            # Определяем все уникальные номера уроков (включая .1)
            all_lessons = set()
            for day in days.values():
                all_lessons.update(day.keys())
            all_lessons_sorted = sorted(all_lessons, key=lambda x: float(x.split('.')[0]) + (0.1 if '.' in x else 0))
            logging.debug(f"Все уроки для класса {class_name}: {all_lessons_sorted}")
            
            # Проходим по каждому уроку
            for lesson_key in all_lessons_sorted:
                logging.debug(f"Обработка урока {lesson_key} в классе {class_name}")
                
                # Создаем строку для текущего урока
                row = ["", lesson_key]  # Первый столбец пустой, второй — номер урока
                
                # Проходим по каждому дню недели
                for day_name, lessons in days.items():
                    logging.debug(f"Проверка дня {day_name} для урока {lesson_key}")
                    
                    # Если урок существует в текущем дне, добавляем его данные
                    lesson_data = lessons.get(lesson_key, {})
                    if lesson_data and lesson_data['lesson']:
                        lesson_info = f"{lesson_data['lesson']}\n{lesson_data['teach']}\n{lesson_data['time']}"
                        if lesson_data['number']:
                            lesson_info += f"\nКабинет: {lesson_data['number']}"
                        row.append(lesson_info)
                    else:
                        row.append("")  # Если урока нет, оставляем пустую ячейку
                    
                    logging.debug(f"Данные урока {lesson_key} в день {day_name} добавлены в строку.")
                
                # Записываем строку с данными урока в CSV
                writer.writerow(row)
                logging.debug(f"Строка для урока {lesson_key} записана в CSV.")
            
            # Добавляем пустую строку между классами для читаемости
            writer.writerow([])
            writer.writerow([])
            logging.debug(f"Добавлены пустые строки после класса {class_name}.")
    
    logging.info(f"CSV-файл успешно создан: {output_csv_path}")

# Путь к JSON-файлу
json_file_path = 'raspisanie_modified.json'
# Путь для сохранения CSV-файла
output_csv_path = 'GIS_schedule.csv'

# Основной блок выполнения скрипта
logging.info("Начало работы скрипта.")
logging.info(f"JSON-файл: {json_file_path}")
logging.info(f"Выходной CSV-файл: {output_csv_path}")

# Создаем CSV-файл
create_csv_schedule(json_file_path, output_csv_path)
logging.info("Работа скрипта завершена.")