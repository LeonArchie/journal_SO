import os

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
    "group.csv",
    "err_groups.log",
    "groups.csv"
]

def delete_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Файл {file_name} удален.")
        else:
            print(f"Файл {file_name} не найден.")
    print("Все файлы удалены.")

if __name__ == "__main__":
    delete_files(files_to_delete)