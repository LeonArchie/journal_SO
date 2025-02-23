import os
import time

# Список файлов для удаления перед стартом
files_to_delete = [
    "log.log",
    "error.log",
    "err_groups.log",
    "final_error.log",
    "chech_groups.log",
    "GIS_schedule.csv",
    "klass.csv",
    "lesson.csv",   
    "raspisanie.csv",
    "groups.csv",
    "zamena.csv",
    "raspisanie.json",
    "raspisanie_key_added.json",
    "raspisanie_sinh_time.json",
    "raspisanie_groups_added.json",
    "raspisanie_null_lesson_added.json",
    "raspisanie_sorted_schedule.json",
    "raspisanie_replace_lessons.json",
    "raspisanie_cab_updated.json"
]

def delete_files(file_list):
    for file_name in file_list:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    time.sleep(2)
    delete_files(files_to_delete)
    time.sleep(5)