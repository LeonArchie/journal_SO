import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from datetime import datetime
import pandas as pd
import subprocess
import os

# Глобальная переменная для хранения всех сообщений
all_log_messages = []

# Открываем файл для записи логов (перезаписываем при каждом запуске)
log_file = open("log.log", "w", encoding="utf-8")

def log_message(message, level):
    """Логирует сообщение с указанным уровнем и временем."""
    global all_log_messages
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    # Добавляем сообщение в глобальный список
    all_log_messages.append((log_entry, level))
    
    # Записываем сообщение в файл
    log_file.write(log_entry + "\n")
    log_file.flush()  # Обеспечиваем запись в файл сразу
    
    # Обновляем лог
    update_log()

def update_log():
    """Обновляет лог на основе выбранного уровня логирования."""
    selected_level = log_level_combobox.get()
    log_area.configure(state="normal")
    log_area.delete("1.0", tk.END)  # Очищаем лог

    # Уровни логирования и их приоритеты
    levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    selected_priority = levels.get(selected_level, 3)  # По умолчанию ERROR

    # Фильтруем сообщения и добавляем только те, которые соответствуют выбранному уровню или выше
    for log_entry, level in all_log_messages:
        if levels.get(level, 3) >= selected_priority:
            log_area.insert(tk.END, log_entry + "\n", level)

    # Применяем цветовую маркировку
    for level in levels:
        log_area.tag_config(level, foreground=get_color_for_level(level))

    log_area.configure(state="disabled")
    log_area.see(tk.END)  # Прокрутка до конца

def filter_logs():
    """Фильтрует сообщения в зависимости от выбранного уровня логирования."""
    update_log()

def get_color_for_level(level):
    """Возвращает цвет для уровня логирования."""
    if level == "INFO":
        return "blue"
    elif level == "ERROR":
        return "red"
    elif level == "DEBUG":
        return "black"
    elif level == "WARNING":
        return "orange"
    else:
        return "black"

def exit_program():
    """Завершение программы."""
    log_message("Завершение программы.", "INFO")
    log_file.close()  # Закрываем файл логов перед выходом
    root.destroy()

def select_schedule_file():
    log_message("Начало выбора файла расписания.", "DEBUG")
    file_path = filedialog.askopenfilename(
        title="Выберите файл расписания",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )
    if file_path:
        schedule_entry.delete(0, tk.END)
        schedule_entry.insert(0, file_path)
        log_message(f"Выбран файл расписания: {file_path}", "INFO")
    else:
        log_message("Выбор файла расписания отменен.", "WARNING")
    check_fields()

def select_reference_file():
    log_message("Начало выбора файла справочника.", "DEBUG")
    file_path = filedialog.askopenfilename(
        title="Выберите файл справочника",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )
    if file_path:
        reference_entry.delete(0, tk.END)
        reference_entry.insert(0, file_path)
        log_message(f"Выбран файл справочника: {file_path}", "INFO")
    else:
        log_message("Выбор файла справочника отменен.", "WARNING")
    check_fields()

def check_fields():
    """Проверяет, заполнены ли все обязательные поля."""
    log_message("Проверка заполнения полей.", "DEBUG")
    if avers_combobox.get() != "Выберите программу" and schedule_entry.get() and reference_entry.get():
        start_button.config(state="normal")
        log_message("Все поля заполнены. Кнопка 'Старт' активирована.", "INFO")
    else:
        start_button.config(state="disabled")
        log_message("Не все поля заполнены. Кнопка 'Старт' неактивна.", "WARNING")

def start_process():
    """Обработка нажатия кнопки 'Старт'."""
    log_message("Начало процесса обработки данных.", "INFO")
    try:
        # Получаем пути к файлам расписания и справочника
        schedule_file = schedule_entry.get()
        reference_file = reference_entry.get()

        # Логируем пути к файлам
        log_message(f"Загрузка файла расписания: {schedule_file}", "DEBUG")
        log_message(f"Загрузка файла справочника: {reference_file}", "DEBUG")

        # Проверяем, что файлы существуют
        if not os.path.exists(schedule_file):
            log_message(f"Файл расписания {schedule_file} не найден.", "ERROR")
            raise FileNotFoundError(f"Файл расписания {schedule_file} не найден.")
        
        if not os.path.exists(reference_file):
            log_message(f"Файл справочника {reference_file} не найден.", "ERROR")
            raise FileNotFoundError(f"Файл справочника {reference_file} не найден.")

        # Вызываем скрипт Leader.py и передаем ему пути к файлам
        log_message("Вызов скрипта Leader.py...", "INFO")
        result = subprocess.run(
            ["python", "Leader.py", schedule_file, reference_file],
            capture_output=True,
            text=True
        )

        # Логируем вывод скрипта Leader.py
        if result.returncode == 0:
            log_message("Скрипт Leader.py успешно выполнен.", "INFO")
            log_message(f"Вывод скрипта: {result.stdout}", "DEBUG")
        else:
            log_message(f"Ошибка при выполнении скрипта Leader.py: {result.stderr}", "ERROR")
            raise RuntimeError(f"Ошибка при выполнении скрипта Leader.py: {result.stderr}")

        # Логируем завершение процесса
        log_message("Обработка данных завершена.", "INFO")

    except Exception as e:
        log_message(f"Ошибка при обработке данных: {e}", "ERROR")
    finally:
        log_message("Завершение процесса обработки данных.", "INFO")

# Создание основного окна
root = tk.Tk()
root.title("JournalSO")
root.resizable(False, False)  # Запрет изменения размера окна

# Установка размера окна
root.geometry("1000x215")  # Ширина 1000, высота 215

# Стилизация
style = ttk.Style()
style.configure("TButton", padding=1, relief="flat", background="#ccc", height=1)
style.configure("TLabel", padding=1, background="#f0f0f0")
style.configure("TEntry", padding=1, relief="flat")
style.configure("TCombobox", padding=1, relief="flat")

# Уровень логирования по умолчанию
log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

# Поле для выбора программы
avers_label = ttk.Label(root, text="Выберите программу:")
avers_label.grid(row=0, column=0, padx=2, pady=1, sticky="w")

# Выпадающий список для выбора программы
avers_combobox = ttk.Combobox(root, values=["Выберите программу", "АВЕРС"], state="readonly", width=30)
avers_combobox.current(0)  # Устанавливаем начальное значение "Выберите программу"
avers_combobox.grid(row=0, column=1, padx=2, pady=1, sticky="ew")

# Поле для выбора файла расписания
schedule_label = ttk.Label(root, text="Расписание:")
schedule_label.grid(row=1, column=0, padx=2, pady=1, sticky="w")

schedule_entry = ttk.Entry(root, width=30)
schedule_entry.grid(row=1, column=1, padx=2, pady=1, sticky="ew")

schedule_button = ttk.Button(root, text="Выбрать файл", command=select_schedule_file)
schedule_button.grid(row=1, column=2, padx=2, pady=1)

# Поле для выбора файла справочника
reference_label = ttk.Label(root, text="Справочник:")
reference_label.grid(row=2, column=0, padx=2, pady=1, sticky="w")

reference_entry = ttk.Entry(root, width=30)
reference_entry.grid(row=2, column=1, padx=2, pady=1, sticky="ew")

reference_button = ttk.Button(root, text="Выбрать файл", command=select_reference_file)
reference_button.grid(row=2, column=2, padx=2, pady=1)

# Кнопка "Старт"
start_button = ttk.Button(root, text="Старт", command=start_process, state="disabled")
start_button.grid(row=3, column=1, pady=2, sticky="ew")

# Кнопка "Выход"
exit_button = ttk.Button(root, text="Выход", command=exit_program)
exit_button.grid(row=3, column=2, padx=2, pady=1, sticky="e")

# Выпадающий список для выбора уровня логирования
log_level_label = ttk.Label(root, text="Уровень логирования:")
log_level_label.grid(row=0, column=3, padx=2, pady=1, sticky="w")

log_level_combobox = ttk.Combobox(root, values=log_levels, state="readonly", width=10)
log_level_combobox.current(log_levels.index("ERROR"))  # По умолчанию ERROR
log_level_combobox.grid(row=0, column=3, padx=2, pady=1, sticky="e")
log_level_combobox.bind("<<ComboboxSelected>>", lambda event: filter_logs())

# Область для вывода сообщений
log_area = scrolledtext.ScrolledText(root, width=65, height=10, state="disabled")
log_area.grid(row=1, column=3, rowspan=3, padx=2, pady=2, sticky="nsew")

# Футер с надписями
footer_frame = ttk.Frame(root)
footer_frame.grid(row=4, column=0, columnspan=4, padx=2, pady=1, sticky="ew")

# Надписи в футере
footer_text = "                                                    Автор: Петунин Лев Михайлович | Email: levmikhailovish@yandex.ru | Версия 2.0 | Apache-2.0 license 2025"
footer_label = ttk.Label(footer_frame, text=footer_text, foreground="gray", justify="center")
footer_label.pack(side="top", fill="x", pady=1)

# Привязка проверки полей к изменению содержимого
avers_combobox.bind("<<ComboboxSelected>>", lambda event: check_fields())
schedule_entry.bind("<KeyRelease>", lambda event: check_fields())
reference_entry.bind("<KeyRelease>", lambda event: check_fields())

# Запуск основного цикла обработки событий
root.mainloop()