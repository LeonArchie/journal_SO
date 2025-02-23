import os
import subprocess
import time

# Список скриптов для запуска
scripts_to_run = [
    ".\\delete.py",
    ".\\exel_to_csv.py",
    ".\\csv_to_json.py",
    ".\\FindError.py",
    ".\\add_key.py",
    ".\\sinh_time.py",
    ".\\add_groups.py",
    ".\\all_null_lesson.py",
    ".\\lesson_sort.py",
    ".\\update_cab.py",
    ".\\check_group.py",
    ".\\update_lesson_gis.py",
    ".\\Final_check.py",
    ".\\json_to_GIS_SO.py"
]

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

# Функция для чтения содержимого файла с указанной кодировкой
def read_file(file_name, encoding="cp1251"):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding=encoding) as file:
            content = file.read()
        return content
    return None

# Функция для обработки ошибок
def handle_error(error_message):
    print(error_message)

# Функция для запроса согласия пользователя
def ask_user_confirmation(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['да', 'yes']:
            return True
        elif user_input in ['нет', 'no']:
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

# Основной код
if __name__ == "__main__":
    # Пауза перед стартом
    print(f"Начинаю работу")
    time.sleep(2)

    for i, script in enumerate(scripts_to_run):
        # Запуск скрипта
        print(f"Скрипт {script} запущен.")
        success = run_script(script)
        if not success:
            handle_error("Остановлено из-за ошибки. Проверьте файл log.log.")
            break

        # Пауза после выполнения скрипта
        print(f"Скрипт {script} выполнен. Ожидание 5 секунд перед следующими проверками...")
        time.sleep(5)

        # Пауза перед проверкой специальных файлов
        print("Проверка специальных файлов через 3 секунды...")
        time.sleep(3)

        # Проверка файла log.log на наличие слова ERROR
        log_content = read_file("log.log")
        if log_content and "ERROR" in log_content:
            print("\nВ файле log.log найдены ошибки")
            if not ask_user_confirmation("Продолжить выполнение? (да/нет): "):
                print("Выполнение скрипта завершено по запросу пользователя.")
                break

        # Проверка наличия error.log или err_groups.log
        error_files = ["error.log", "err_groups.log", "chech_groups.log", "final_error.log"]
        files_found = [file for file in error_files if os.path.exists(file)]
        if files_found:
            print(f"Найдены следующие файлы ошибок: {', '.join(files_found)}.")
            if not ask_user_confirmation("Продолжить выполнение? (да/нет): "):
                print("Выполнение скрипта завершено по запросу пользователя.")
                break

        # Закрытие всех файлов перед уведомлением пользователя
        print("Закрытие всех открытых файлов...")
        time.sleep(3)

    print("Выполнение скрипта завершено.")