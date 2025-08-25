import htmlgenerator as hg
import os
import random
from pathlib import Path
import tkinter as tk
from tkinter import messagebox



def create_bingo_files():
    css_styles = """
    /* Общие стили для страницы, чтобы карточка была по центру */
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px; /* Добавим отступ, чтобы карточка не прилипала к краям */
        background-color: #f0f0f0; /* Слегка серый фон для страницы */
        box-sizing: border-box;
    }

    /* Контейнер для всей карточки бинго */
    .bingo-card {
        width: 396px;
        height: 396px;
        background-color: #FFB200; 
    
        /* Используем Grid для создания идеальной сетки 5x5 */
        display: grid;
        /* 5 колонок по 72px и 5 рядов по 72px */
        grid-template-columns: repeat(5, 72px);
        grid-template-rows: repeat(5, 72px);
    
        /* Расстояние между ячейками. */
        gap: 3px;
    
        /* Выравниваем сетку по центру, если контейнер вдруг станет больше */
        justify-content: center;
        align-content: center;

    
    }

    /* Стиль для каждой отдельной ячейки */
    .cell {
        background-color: #ffffff; /* Белый фон для ячеек */
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    """
    try:
        number_of_copies = int(entry_copies.get())
        if number_of_copies <= 0:
            messagebox.showerror("Ошибка", "Количество карточек должно быть положительным числом.")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Количество карточек должно быть целым числом.")
        return    
    words_raw = text_words.get("1.0", tk.END)
    source_words = words_raw.strip().splitlines()

    words_raw = text_words.get("1.0", tk.END)
    source_words = words_raw.strip().splitlines()

    if len(source_words) != 25:
        messagebox.showwarning("Внимание", f"Нужно ровно 25 фраз, а вы ввели {len(source_words)}.")
        return

    directory_name = "output_cards"
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")

    # Здесь хранятся уникальные комбинации карточек
    generated_cards = set()

    while len(generated_cards) < number_of_copies:
        words_to_shuffle = source_words.copy()
        random.shuffle(words_to_shuffle)
        card_layout = tuple(words_to_shuffle)

        if card_layout in generated_cards:
            continue
        
        generated_cards.add(card_layout)

      # 6. Создаем HTML-структуру для этой карточки
    
    # 6.1. Сначала генерируем список из 25 HTML-ячеек
        bingo_cells = [hg.DIV(word, _class="cell") for word in card_layout]
        
        page_layout = hg.HTML(
            hg.HEAD(
                hg.META(charset="utf-8"),
                hg.TITLE("Bingo Card"),
                # Путь к файлу с настройками стиля
                hg.STYLE(css_styles) 
            ),
            hg.BODY(
                hg.DIV(
                    *bingo_cells,  
                    _class="bingo-card"
                )
            )
        )
        
        
        html_content = hg.render(page_layout, {})
        
        
        card_number = len(generated_cards)
        file_name = f"card_{card_number}.html"
        file_path = Path(directory_name) / file_name
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл {file_path}: {e}")
            return

    messagebox.showinfo("Готово", f"Успешно создано {number_of_copies} карточек в папке '{directory_name}'!")

window = tk.Tk()
window.title("Генератор Бинго")
window.geometry("400x400")

main_frame = tk.Frame(window, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

label_copies = tk.Label(main_frame, text="Количество карточек для генерации:")
label_copies.pack(pady=(0, 5))
entry_copies = tk.Entry(main_frame)
entry_copies.pack(fill="x", pady=(0, 10))

label_words = tk.Label(main_frame, text="Введите 25 фраз (каждая с новой строки):")
label_words.pack(pady=(0, 5))
text_words = tk.Text(main_frame, height=10) 
text_words.pack(fill="both", expand=True, pady=(0, 10))


generate_button = tk.Button(main_frame, text="Создать карточки", command=create_bingo_files)
generate_button.pack()

window.mainloop()
