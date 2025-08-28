import os  # Модуль для взаимодействия с операционной системой (создание папок)
import random  # Модуль для перемешивания элементов
from pathlib import Path  # Модуль для удобной работы с путями к файлам
import re  # Модуль для работы с регулярными выражениями
import tkinter as tk 
from tkinter import Entry # Библиотека для создания графического интерфейса
from tkinter import messagebox  # Модуль для отображения всплывающих окон

# --- Глобальные переменные и константы ---
# Списки с путями к изображениям для разных раундов
OUTPUT_DIR = "output_cards"
round_images = ["../assets/round1.png", "../assets/round2.png", "../assets/round3.png"]
background_images = ["../assets/background1.png", "../assets/background2.png", "../assets/background3.png"]

def _build_card_html(layout, round_image_path, background_image_path):
    """
    Создает HTML-код для одной карточки бинго на основе раскладки и путей к изображениям.

    Аргументы:
        layout (tuple): Кортеж из 25 фраз для размещения на карточке.
        round_image_path (str): Путь к изображению номера раунда.
        background_image_path (str): Путь к фоновому изображению.

    Возвращает:
        str: Готовая HTML-строка для карточки.
    """
    cells_html_list = []
    for word in layout:
        cells_html_list.append(f'<div class="cell">{word}</div>')
    all_cells_html = "".join(cells_html_list)

    final_html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title> Карточка бинго </title>
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <div class="whole-card" style="background-image: url('{background_image_path}');">
            
            <div class="header">
                <img src="../assets/rules.png" class="rules">
                <img src="../assets/logo.png" class="logo">
                <img src="{round_image_path}" class="tour-number">
            </div>

            <div class="main-grid">
                <div class="bingo-card">
                    {all_cells_html}
                </div>
            </div>

            <div class="footer">
                <div class="qr-code-stdup">
                    <img src="../assets/qr-code-stdup.png">
                </div>
                <div class="footer-contacts">
                    <img src="../assets/contacts.png">
                </div>
                <div class="qr-code-muz">
                    <img src="../assets/qr-code-muz.png">
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return final_html

def _get_user_inputs():
    """
    Извлекает и проверяет данные, введенные пользователем в GUI.
    Показывает сообщения об ошибках, если данные некорректны.

    Возвращает:
        tuple: Кортеж с (количеством копий, номером раунда, списком фраз) в случае успеха.
        None: Если проверка не пройдена.
    """
    try:
        number_of_copies = int(entry_copies.get())
        number_of_round = int(entry_round.get())
        if number_of_copies <= 0:
            messagebox.showerror("Ошибка", "Количество карточек должно быть положительным числом.")
            return None
        if not (1 <= number_of_round <= len(round_images)):
            messagebox.showerror("Ошибка", f"Номер раунда должен быть от 1 до {len(round_images)}.")
            return None
    except ValueError:
        messagebox.showerror("Ошибка", "Количество карточек и номер раунда должны быть целыми числами.")
        return None

    words_raw = text_words.get("1.0", tk.END)
    source_words = re.findall(r"\n", words_raw)
    if len(source_words) != 25:
        messagebox.showwarning("Внимание", f"Нужно ровно 25 фраз, а вы ввели {len(source_words)}.")
        return None

    return number_of_copies, number_of_round, source_words

def _generate_unique_layouts(words, count):
    """
    Генерирует заданное количество уникальных, перемешанных раскладок карточек.

    Аргументы:
        words (list): Список из 25 исходных фраз.
        count (int): Количество уникальных раскладок для генерации.

    Возвращает:
        list: Список кортежей, где каждый кортеж - это уникальная раскладка.
    """
    generated_cards = set()
    # Цикл работает, пока не будет создано нужное количество УНИКАЛЬНЫХ карточек
    while len(generated_cards) < count:
        words_to_shuffle = words.copy()
        random.shuffle(words_to_shuffle)
        card_layout = tuple(words_to_shuffle)
        generated_cards.add(card_layout)
    return list(generated_cards)

def _save_html_file(content, path):
    """
    Сохраняет HTML-содержимое в файл.

    Аргументы:
        content (str): HTML-строка для сохранения.
        path (Path): Объект Path, представляющий путь к файлу.

    Возвращает:
        bool: True в случае успеха, False в случае ошибки.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл {path}: {e}")
        return False

# Основная функция, которая запускается при нажатии на кнопку
def create_bingo_files():
    """
    Главная функция-координатор. Получает данные, генерирует карточки и сохраняет их.
    """
    # 1. Получение и проверка данных от пользователя
    user_inputs = _get_user_inputs()
    if not user_inputs:
        return
    number_of_copies, number_of_round, source_words = user_inputs

    # 2. Создание папки для сохранения карточек
    try:
        os.mkdir(OUTPUT_DIR)
        print(f"Directory '{OUTPUT_DIR}' created successfully.")
    except FileExistsError:
        print(f"Directory '{OUTPUT_DIR}' already exists.")

    # 3. Генерация уникальных раскладок карточек
    layouts = _generate_unique_layouts(source_words, number_of_copies)

    # 4. Создание и сохранение HTML-файлов
    image_index = number_of_round - 1
    round_image = round_images[image_index]
    background_image = background_images[image_index]

    for i, layout in enumerate(layouts):
        html_content = _build_card_html(layout, round_image, background_image)
        file_path = Path(OUTPUT_DIR) / f"card_{i + 1}.html"
        if not _save_html_file(html_content, file_path):
            break  # Прерываем цикл, если сохранение не удалось

    else:  # Этот блок выполнится, если цикл завершился без 'break'
        # 5. Сообщение об успешном завершении
        messagebox.showinfo("Готово", f"Успешно создано {number_of_copies} карточек в папке '{OUTPUT_DIR}'!")

def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

# --- Создание графического интерфейса (GUI) ---
window = tk.Tk()
window.title("Генератор Бинго")
window.geometry("400x400")
window.bind_all("<Key>", _onKeyRelease, "+")

# Создаем главный фрейм (рамку) с отступами
main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

# Элементы для ввода количества карточек
label_copies = tk.Label(main_frame, text="Количество карточек для генерации:")
label_copies.pack(pady=(0, 5))
entry_copies = tk.Entry(main_frame)
entry_copies.pack(fill="x", pady=(0, 10))
# Элементы для ввода номера раунда
round_number = tk.Label(main_frame, text="Номер раунда (1,2 или 3):")
round_number.pack(pady=(0, 5))
entry_round = tk.Entry(main_frame)
entry_round.pack(fill="x", pady=(0, 10))

# Элементы для ввода фраз для бинго
label_words = tk.Label(main_frame, text="Введите 25 фраз (Каждая с новой строки):")
label_words.pack(pady=(0, 5))
text_words = tk.Text(main_frame, height=10)
text_words.pack(fill="both", expand=True, pady=(0, 10))


# --- Создание контекстного меню для текстового поля ---
def show_context_menu(event):
    # Создаем меню
    context_menu = tk.Menu(main_frame, tearoff=0)
    # Добавляем команды "Вырезать", "Копировать", "Вставить"
    context_menu.add_command(label="Вырезать", command=lambda: event.widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Копировать", command=lambda: event.widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Вставить", command=lambda: event.widget.event_generate("<<Paste>>"))
    # Показываем меню в месте клика мыши
    context_menu.tk_popup(event.x_root, event.y_root)

# Привязываем правый клик мыши (<Button-3>) к функции показа меню
text_words.bind("<Button-3>", show_context_menu)

# Кнопка, которая запускает функцию create_bingo_files
generate_button = tk.Button(main_frame, text="Создать карточки", command=create_bingo_files)
generate_button.pack()


# Запуск главного цикла обработки событий окна
window.mainloop()
