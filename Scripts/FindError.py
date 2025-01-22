import json
import csv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Функция для загрузки предметов из файла Spravosh.csv
def load_subjects(file_path):
    """
    Загружает список допустимых предметов из файла Spravosh.csv.
    Файл должен быть в кодировке cp1251 (Windows-1251).
    Первые две строки файла игнорируются, так как они содержат заголовки.
    Возвращает список предметов.
    """
    subjects = []  # Создаем пустой список для хранения предметов
    logging.info(f"Загрузка предметов из файла: {file_path}")
    
    # Открываем файл Spravosh.csv для чтения
    with open(file_path, 'r', encoding='cp1251') as file:
        reader = csv.reader(file, delimiter=';')  # Используем разделитель ';'
        
        # Проходим по каждой строке файла
        for i, row in enumerate(reader):
            if i >= 2:  # Игнорируем первые две строки (заголовки)
                subject = row[0].strip()  # Убираем лишние пробелы и добавляем предмет в список
                subjects.append(subject)
                logging.debug(f"Добавлен предмет: {subject}")
    
    logging.info(f"Загружено {len(subjects)} предметов.")
    return subjects

# Функция для проверки расписания
def check_schedule(schedule, subjects, error_file_path):
    """
    Проверяет расписание на наличие предметов, которые не указаны в списке допустимых.
    Если найден недопустимый предмет, он заменяется на пустые значения, а информация об ошибке записывается в файл.
    Возвращает True, если найдены ошибки, иначе False.
    """
    errors_found = False  # Флаг для отслеживания наличия ошибок
    logging.info(f"Начало проверки расписания. Ошибки будут записаны в файл: {error_file_path}")
    
    # Открываем файл для записи ошибок
    with open(error_file_path, 'w', encoding='utf-8') as error_file:
        # Проходим по каждому классу в расписании
        for class_name, days in schedule.items():
            logging.info(f"Проверка класса: {class_name}")
            
            # Проходим по каждому дню недели
            for day, lessons in days.items():
                logging.info(f"Проверка дня: {day}")
                
                # Проходим по каждому уроку в дне
                for lesson_num, lesson_data in lessons.items():
                    lesson_subject = lesson_data["Урок"]  # Получаем название предмета
                    
                    # Проверяем, есть ли предмет в списке допустимых
                    if lesson_subject not in subjects:
                        # Если предмет не найден, заменяем все значения на пустоту
                        schedule[class_name][day][lesson_num] = {
                            "Время": "",
                            "Урок": "",
                            "Кабинет": "",
                            "Учитель": ""
                        }
                        
                        # Записываем ошибку в файл
                        error_file.write(f"{{ОШИБКА}} Класс - {class_name} - {day} - Номер урока {lesson_num}\n")
                        error_file.write(f"{json.dumps(lesson_data, ensure_ascii=False, indent=4)}\n\n")
                        
                        # Логируем ошибку в консоль и в файл app.log
                        logging.error(f"Найдена ошибка в классе {class_name}, день {day}, урок {lesson_num}")
                        logging.error(f"Недопустимый предмет: {lesson_subject}")
                        errors_found = True
                    else:
                        # Если предмет корректен, логируем успешную проверку
                        logging.debug(f"Урок {lesson_num} в классе {class_name}, день {day} корректен. Предмет: {lesson_subject}")
    
    # Логируем итог проверки
    if errors_found:
        logging.info("Проверка завершена. Найдены ошибки.")
    else:
        logging.info("Проверка завершена. Ошибок не найдено.")
    
    return errors_found

# Пути к файлам
spravosh_file_path = '/home/archie/EDU/Spravosh.csv'  # Путь к файлу с предметами
schedule_file_path = '/home/archie/EDU/schedule.json'  # Путь к файлу с расписанием
error_file_path = '/home/archie/EDU/error.txt'  # Путь к файлу для записи ошибок

# Основной блок выполнения скрипта
logging.info("Начало работы скрипта.")

# Загружаем предметы из Spravosh.csv
logging.info(f"Загрузка предметов из файла: {spravosh_file_path}")
subjects = load_subjects(spravosh_file_path)

# Загружаем JSON с расписанием
logging.info(f"Загрузка расписания из файла: {schedule_file_path}")
with open(schedule_file_path, 'r', encoding='utf-8') as file:
    schedule = json.load(file)
logging.info("Расписание успешно загружено.")

# Проверяем расписание
logging.info("Начало проверки расписания.")
errors_found = check_schedule(schedule, subjects, error_file_path)

# Сохраняем обновленный JSON (если были ошибки)
if errors_found:
    logging.info(f"Сохранение обновленного расписания в файл: {schedule_file_path}")
    with open(schedule_file_path, 'w', encoding='utf-8') as file:
        json.dump(schedule, file, ensure_ascii=False, indent=4)
    logging.info("Обновленное расписание сохранено.")
else:
    logging.info("Расписание не требует изменений.")

# Выводим итоговый отчет
if errors_found:
    logging.info("ПРОВЕРЕНО - НАЙДЕНЫ ОШИБКИ")
else:
    logging.info("ПРОВЕРЕНО - Ошибок не найдено")

logging.info("Работа скрипта завершена.")