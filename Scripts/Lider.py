import os
import subprocess
import time  # Импортируем модуль time для использования sleep

# Список файлов для удаления перед стартом
files_to_delete = [
    "GIS_schedule.csv",
    "klass.csv",
    "lesson.csv",
    "log.log",
    "raspisanie.csv",
    "raspisanie.json",
    "raspisanie_modified.json",
    "error.log",
    "group.csv"
]

# Список скриптов для запуска
scripts_to_run = [
    ".\\exel_to_csv.py",
    ".\\csv_to_json.py",
    ".\\FindError.py",
    ".\\normalization.py",
    ".\\json_to_GIS_SO.py"
]

# Функция для удаления файлов
def delete_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Файл {file_name} удален.")
    print("Все файлы удалены. Ожидание 3 секунды перед продолжением...")
    time.sleep(3)  # Добавляем таймаут после удаления файлов

# Функция для запуска скрипта и проверки его выполнения
def run_script(script_path):
    try:
        result = subprocess.run(["python", script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Скрипт {script_path} выполнен успешно.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении скрипта {script_path}:")
        print(e.stderr)
        return False

# Основной код
if __name__ == "__main__":
    # Удаление файлов перед началом
    delete_files(files_to_delete)

    # Запуск скриптов по очереди
    for i, script in enumerate(scripts_to_run):
        if i > 0 and not os.path.exists("error.log"):  # Проверяем наличие error.log перед FindError.py
            success = run_script(script)
            if not success:
                print("Остановлено из-за ошибки. Проверьте файл log.log.")
                if os.path.exists("log.log"):
                    with open("log.log", "r", encoding="cp1251") as log_file:  # Открываем log.log в CP1251
                        print("\nСодержимое файла log.log:")
                        print(log_file.read())
                break
            print(f"Скрипт {script} выполнен. Ожидание 3 секунды перед запуском следующего скрипта...")
            time.sleep(3)  # Добавляем таймаут между скриптами
        elif script == ".\\FindError.py":
            success = run_script(script)
            if not success:
                print("Остановлено из-за ошибки. Проверьте файл log.log.")
                if os.path.exists("log.log"):
                    with open("log.log", "r", encoding="cp1251") as log_file:  # Открываем log.log в CP1251
                        print("\nСодержимое файла log.log:")
                        print(log_file.read())
                break
            print(f"Скрипт {script} выполнен. Ожидание 3 секунды перед запуском следующего скрипта...")
            # Проверка наличия error.log после FindError.py
            if os.path.exists("error.log"):
                print("Найден файл error.log. Выполнение прекращено.")
                with open("error.log", "r", encoding="cp1251") as error_file:  # Открываем error.log в CP1251
                    print("\nСодержимое файла error.log:")
                    print(error_file.read())
                break
            print(f"Скрипт {script} выполнен. Ожидание 3 секунды перед запуском следующего скрипта...")
            time.sleep(3)  # Добавляем таймаут между скриптами
        else:
            success = run_script(script)
            if not success:
                print("Остановлено из-за ошибки. Проверьте файл log.log.")
                if os.path.exists("log.log"):
                    with open("log.log", "r", encoding="cp1251") as log_file:  # Открываем log.log в CP1251
                        print("\nСодержимое файла log.log:")
                        print(log_file.read())
                break
            print(f"Скрипт {script} выполнен. Ожидание 3 секунды перед запуском следующего скрипта...")
            time.sleep(3)  # Добавляем таймаут между скриптами

    print("Выполнение скрипта завершено.")