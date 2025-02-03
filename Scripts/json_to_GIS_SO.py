import json
import csv
import logging

# Настройка логирования
logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def create_csv_schedule(json_file_path, output_csv_path):
    """
    Преобразует JSON-файл с расписанием в CSV-файл.
    """
    logging.info("Начало работы функции create_csv_schedule.")
    
    try:
        # Загружаем JSON-файл с расписанием
        with open(json_file_path, 'r', encoding='utf-8') as file:
            schedule = json.load(file)
        logging.info(f"JSON-файл успешно загружен: {json_file_path}.")
    except FileNotFoundError:
        logging.error(f"Файл {json_file_path} не найден.")
        return
    except json.JSONDecodeError:
        logging.error(f"Ошибка декодирования JSON в файле {json_file_path}.")
        return

    # Создаем CSV-файл
    try:
        with open(output_csv_path, 'w', encoding='windows-1251', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            for class_name, days in schedule.items():
                logging.info(f"Обработка класса: {class_name}")
                
                # Записываем заголовок класса
                writer.writerow([f"Класс: {class_name}"])
                writer.writerow([])  # Пустая строка для читаемости
                
                # Записываем заголовки дней недели
                writer.writerow(["", "", "Пн", "Вт", "Ср", "Чт", "Пт"])
                writer.writerow([])  # Пустая строка
                
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
                        
                        # Инициализируем ячейку как пустую строку
                        cell_content = ""
                        
                        if all(key in lesson_data for key in ['lesson', 'teach', 'time']):
                            # Собираем основные данные
                            cell_content = f"{lesson_data['lesson']}\n{lesson_data['teach']}\n{lesson_data['time']}"
                            
                            # Добавляем номер кабинета, если он есть
                            if lesson_data.get('number'):
                                cell_content += f"\n{lesson_data['number']}"
                            
                            # Добавляем группы, если они указаны
                            if lesson_data.get('groups'):
                                cell_content += f"\n{lesson_data['groups']}"
                        
                        # Убираем лишний перенос строки в конце
                        cell_content = cell_content.rstrip('\n')
                        
                        # Если ячейка пустая, оставляем ее такой
                        row.append(cell_content if cell_content else "")
                        
                        logging.debug(f"Данные урока {lesson_key} в день {day_name} добавлены в строку.")
                    
                    # Записываем строку с данными урока в CSV
                    writer.writerow(row)
                    logging.debug(f"Строка для урока {lesson_key} записана в CSV.")
                
                # Добавляем пустые строки между классами для читаемости
                writer.writerow([])
                writer.writerow([])
                logging.debug(f"Добавлены пустые строки после класса {class_name}.")
        
        logging.info(f"CSV-файл успешно создан: {output_csv_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании CSV-файла: {e}")

# Путь к JSON-файлу
json_file_path = 'raspisanie_modified.json'

# Путь для сохранения CSV-файла
output_csv_path = 'GIS_schedule.csv'

# Основной блок выполнения скрипта
if __name__ == "__main__":
    logging.info("Начало работы скрипта.")
    logging.info(f"JSON-файл: {json_file_path}")
    logging.info(f"Выходной CSV-файл: {output_csv_path}")
    
    # Создаем CSV-файл
    create_csv_schedule(json_file_path, output_csv_path)
    
    logging.info("Работа скрипта завершена.")