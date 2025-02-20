import os
import subprocess
import time

# Список скриптов для запуска
scripts_to_run = [
    ".\\delete.py",
    ".\\exel_to_csv.py",
    ".\\csv_to_json.py",
    ".\\FindError.py",
    ".\\normalization.py",
    ".\\check_group.py",
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
            return file.read()
    return None

# Функция для обработки ошибок
def handle_error(error_message, log_file="log.log"):
    print(error_message)
    log_content = read_file(log_file)
    if log_content:
        print("\nСодержимое файла log.log:")
        print(log_content)

# Основной код
if __name__ == "__main__":
    for i, script in enumerate(scripts_to_run):
        # Запуск скрипта
        success = run_script(script)
        if not success:
            handle_error("Остановлено из-за ошибки. Проверьте файл log.log.")
            break

        # Проверка наличия error.log после FindError.py
        if script == ".\\FindError.py":
            if os.path.exists("error.log"):
                error_content = read_file("error.log")
                print("Найден файл error.log. Выполнение прекращено.")
                if error_content:
                    print("\nСодержимое файла error.log:")
                    print(error_content)
                break

        # Вывод сообщения о завершении скрипта и таймаут
        print(f"Скрипт {script} выполнен. Ожидание 3 секунды перед запуском следующего скрипта...")
        time.sleep(3)


    print("Выполнение скрипта завершено.")