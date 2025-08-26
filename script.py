import htmlgenerator as hg  # Библиотека для генерации HTML-кода
import os  # Модуль для взаимодействия с операционной системой (создание папок)
import random  # Модуль для перемешивания элементов
from pathlib import Path  # Модуль для удобной работы с путями к файлам
import tkinter as tk  # Библиотека для создания графического интерфейса
from tkinter import messagebox  # Модуль для отображения всплывающих окон



# Основная функция, которая запускается при нажатии на кнопку
def create_bingo_files():
    # --- 1. Получение и проверка данных из полей ввода ---

    try:
        number_of_copies = int(entry_copies.get())
        if number_of_copies <= 0:
            messagebox.showerror("Ошибка", "Количество карточек должно быть положительным числом.")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Количество карточек должно быть целым числом.")
        return

    # Получаем текст из большого текстового поля
    words_raw = text_words.get("1.0", tk.END)
    # Убираем лишние пробелы и разделяем текст на строки
    source_words = words_raw.strip().splitlines()

    # Проверяем, что введено ровно 25 фраз
    if len(source_words) != 25:
        messagebox.showwarning("Внимание", f"Нужно ровно 25 фраз, а вы ввели {len(source_words)}.")
        return

    # --- 2. Создание папки для сохранения карточек ---
    directory_name = "output_cards"
    try:
        os.mkdir(directory_name)  # Пытаемся создать папку
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")

    # Здесь хранятся уникальные комбинации карточек
    generated_cards = set()

    # --- 3. Основной цикл генерации карточек ---
    while len(generated_cards) < number_of_copies:
        # Создаем копию исходного списка, чтобы не изменять его
        words_to_shuffle = source_words.copy()
        # Перемешиваем фразы в случайном порядке
        random.shuffle(words_to_shuffle)
        # Превращаем список в кортеж, чтобы его можно было добавить в set
        card_layout = tuple(words_to_shuffle)

        # Если такая комбинация уже была создана, пропускаем итерацию
        if card_layout in generated_cards:
            continue

        # Добавляем новую уникальную комбинацию в set
        generated_cards.add(card_layout)

        # --- 4. Создание HTML-структуры для карточки ---

        # Генерируем список из 25 HTML-ячеек (<div>)
        bingo_cells = [hg.DIV(word, _class="cell") for word in card_layout]

        # --- 4. Создание HTML-структуры ---
        bingo_cells = [hg.DIV(word, _class="cell") for word in card_layout]

        page_layout = hg.HTML(
            hg.HEAD(
                hg.META(charset="utf-8"),
                hg.TITLE("Bingo Card"),
                hg.LINK(rel="stylesheet", href="../style.css")
            ),
            hg.BODY(
                # Главный контейнер, внутри которого лежат все 3 блока
                hg.DIV(
                    # Блок 1: Шапка
                    hg.DIV(
                        hg.DIV(
                            hg.IMG(src="../assets/музло1.png", _class="rule-box"),
                            hg.IMG(src="../assets/музло2.png", _class="rule-box"),
                            hg.IMG(src="../assets/музло3.png", _class="rule-box"),
                            _class="rules-container"
                        ),
                        hg.IMG(src="../assets/logo.png", _class="logo"),
                        hg.DIV("ТУР №1", _class="tour-number"),
                        _class="header"
                    ),

                    # Блок 2: Основная сетка
                    hg.DIV(
                        hg.DIV(*bingo_cells, _class="bingo-card"),
                        _class="main-grid"
                    ),

                    # Блок 3: Подвал
                    hg.DIV(
                        hg.DIV(
                            hg.IMG(src="../assets/qr-code.png", _class="qr-code"),
                            hg.P("QR МУЗЛО"),
                            _class="footer-item"
                        ),
                        hg.DIV(
                            hg.P("Контакты"),
                            _class="footer-item"
                        ),
                        hg.DIV(
                            hg.IMG(src="../assets/qr-code.png", _class="qr-code"),
                            hg.P("QR STANDUP"),
                            _class="footer-item"
                        ),
                        _class="footer"
                    ),
                    _class="whole-card"
                )
            )
        )
        
        # Превращаем Python-объект в готовую HTML-строку
        html_content = hg.render(page_layout, {})

        # --- 5. Сохранение HTML-файла ---
        card_number = len(generated_cards)
        file_name = f"card_{card_number}.html"
        file_path = Path(directory_name) / file_name

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл {file_path}: {e}")
            return
    # --- 6. Показываем сообщение об успешном завершении ---
    messagebox.showinfo("Готово", f"Успешно создано {number_of_copies} карточек в папке '{directory_name}'!")

# --- Создание графического интерфейса (GUI) ---
window = tk.Tk()
window.title("Генератор Бинго")
window.geometry("400x400")

# Создаем главный фрейм (рамку) с отступами
main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

# Элементы для ввода количества карточек
label_copies = tk.Label(main_frame, text="Количество карточек для генерации:")
label_copies.pack(pady=(0, 5))
entry_copies = tk.Entry(main_frame)
entry_copies.pack(fill="x", pady=(0, 10))

# Элементы для ввода фраз для бинго
label_words = tk.Label(main_frame, text="Введите 25 фраз (каждая с новой строки):")
label_words.pack(pady=(0, 5))
text_words = tk.Text(main_frame, height=10)
text_words.pack(fill="both", expand=True, pady=(0, 10))

# Кнопка, которая запускает функцию create_bingo_files
generate_button = tk.Button(main_frame, text="Создать карточки", command=create_bingo_files)
generate_button.pack()

# Запуск главного цикла обработки событий окна
window.mainloop()
