import json
import csv
import logging

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def create_csv_schedule(json_file_path, output_csv_path):
    """
    Преобразует JSON-файл с расписанием в CSV-файл, который может быть использован в системе GIS.
    CSV-файл создается в кодировке Windows-1251, а данные разделяются символом ';'.
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
        logging.info("CSV-файл открыт для записи.")

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

            # Определяем максимальное количество уроков в классе
            max_lessons = max(len(days[day]) for day in days)
            logging.debug(f"Максимальное количество уроков в классе {class_name}: {max_lessons}")

            # Проходим по каждому уроку
            for lesson_num in range(1, max_lessons + 1):
                logging.debug(f"Обработка урока {lesson_num} в классе {class_name}")

                # Создаем строку для текущего урока
                row = ["", lesson_num]  # Первый столбец пустой, второй — номер урока

                # Проходим по каждому дню недели
                for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]:
                    logging.debug(f"Проверка дня {day} для урока {lesson_num}")

                    # Если урок существует в текущем дне, добавляем его данные
                    if str(lesson_num) in days[day]:
                        lesson_data = days[day][str(lesson_num)]
                        lesson_info = f"{lesson_data['Урок']}\n{lesson_data['Учитель']}\n{lesson_data['Время']}"
                        
                        # Если указан кабинет, добавляем его в информацию об уроке
                        if lesson_data['Кабинет']:
                            lesson_info += f"\nКабинет: {lesson_data['Кабинет']}"
                        
                        row.append(lesson_info)
                        logging.debug(f"Данные урока {lesson_num} в день {day} добавлены в строку.")
                    else:
                        # Если урока нет, оставляем пустую ячейку
                        row.append("")
                        logging.debug(f"Урок {lesson_num} в день {day} отсутствует. Добавлена пустая ячейка.")

                # Записываем строку с данными урока в CSV
                writer.writerow(row)
                logging.debug(f"Строка для урока {lesson_num} записана в CSV.")

            # Добавляем пустую строку между классами для читаемости
            writer.writerow([])
            writer.writerow([])
            logging.debug(f"Добавлены пустые строки после класса {class_name}.")

    logging.info(f"CSV-файл успешно создан: {output_csv_path}")

# Путь к JSON-файлу
json_file_path = '/home/archie/EDU/schedule.json'

# Путь для сохранения CSV-файла
output_csv_path = '/home/archie/EDU/GIS.csv'

# Основной блок выполнения скрипта
logging.info("Начало работы скрипта.")
logging.info(f"JSON-файл: {json_file_path}")
logging.info(f"Выходной CSV-файл: {output_csv_path}")

# Создаем CSV-файл
create_csv_schedule(json_file_path, output_csv_path)

logging.info("Работа скрипта завершена.")