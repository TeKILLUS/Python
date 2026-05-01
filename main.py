import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Book Tracker")
        self.root.geometry("800x500")
        
        self.all_books = []  # Полный список книг
        self.data_file = "books.json"
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # --- Поля ввода ---
        input_frame = ttk.LabelFrame(self.root, text="Добавить книгу", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        fields = [
            ("Название:", "title"),
            ("Автор:", "author"),
            ("Жанр:", "genre"),
            ("Кол-во страниц:", "pages")
        ]
        self.entries = {}
        for i, (label_text, key) in enumerate(fields):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5)
            entry = ttk.Entry(input_frame, width=30)
            entry.grid(row=i, column=1, padx=5)
            self.entries[key] = entry

        # --- Кнопки управления ---
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="➕ Добавить книгу", command=self.add_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Сохранить", command=self.save_data).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Загрузить", command=self.load_data).pack(side="left", padx=5)

        # --- Фильтры ---
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Жанр:").pack(side="left", padx=5)
        self.genre_filter = ttk.Combobox(filter_frame, state="readonly", width=15)
        self.genre_filter.pack(side="left", padx=5)

        ttk.Label(filter_frame, text="Страниц >").pack(side="left", padx=5)
        self.pages_filter = ttk.Entry(filter_frame, width=8)
        self.pages_filter.pack(side="left", padx=5)

        ttk.Button(filter_frame, text="🔍 Применить", command=self.apply_filter).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="❌ Сбросить", command=self.reset_filter).pack(side="left", padx=5)

        # --- Таблица ---
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страниц")
        self.tree.pack(fill="both", expand=True)

    def validate_input(self):
        title = self.entries["title"].get().strip()
        author = self.entries["author"].get().strip()
        genre = self.entries["genre"].get().strip()
        pages_str = self.entries["pages"].get().strip()

        if not all([title, author, genre, pages_str]):
            messagebox.showerror("Ошибка ввода", "Все поля должны быть заполнены!")
            return None

        # ИСПРАВЛЕНО: Проверяем что число И больше 0
        if not pages_str.isdigit() or int(pages_str) <= 0:
            messagebox.showerror("Ошибка ввода", "Количество страниц должно быть числом больше 0!")
            return None

        return {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages_str)
        }

    def add_book(self):
        book = self.validate_input()
        if book is None:
            return

        self.all_books.append(book)
        self.update_table(self.all_books)
        
        # ИСПРАВЛЕНО: Обновляем список жанров после добавления
        self.update_genre_combo()
        
        self.clear_fields()
        messagebox.showinfo("Успех", "Книга добавлена в список!")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def apply_filter(self):
        genre = self.genre_filter.get().strip()
        pages_limit = self.pages_filter.get().strip()

        filtered = self.all_books
        if genre:
            filtered = [b for b in filtered if b["genre"].lower() == genre.lower()]
        if pages_limit.isdigit():
            min_pages = int(pages_limit)
            filtered = [b for b in filtered if b["pages"] > min_pages]

        self.update_table(filtered)

    def reset_filter(self):
        self.genre_filter.set("")
        self.pages_filter.delete(0, tk.END)
        self.update_table(self.all_books)

    def save_data(self):
        if not self.all_books:
            messagebox.showwarning("Внимание", "Нет данных для сохранения!")
            return
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.all_books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены в books.json")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_data(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.all_books = json.load(f)
            self.update_table(self.all_books)
            self.update_genre_combo()
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

    def update_genre_combo(self):
        """Обновляет список жанров в выпадающем списке"""
        genres = sorted(set(b["genre"] for b in self.all_books))
        self.genre_filter["values"] = genres

    def update_table(self, books_list):
        """Обновляет таблицу с книгами"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in books_list:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
