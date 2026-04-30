import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Ввод данных
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Дата (гггг-мм-дд):").grid(row=0, column=0)
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=0, column=1)

        ttk.Label(form_frame, text="Тип тренировки:").grid(row=1, column=0)
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=1, column=1)

        ttk.Label(form_frame, text="Длительность (мин):").grid(row=2, column=0)
        self.duration_entry = ttk.Entry(form_frame)
        self.duration_entry.grid(row=2, column=1)

        ttk.Button(self.root, text="Добавить тренировку", command=self.add_training).pack(pady=5)

        # Фильтр
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.filter_type = ttk.Entry(filter_frame)
        self.filter_type.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=1, column=0)
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.grid(row=1, column=1)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=2, column=0, pady=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data).grid(row=2, column=1, pady=5)

        # Таблица для тренировок
        self.tree = ttk.Treeview(self.root, columns=("date", "type", "duration"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность")
        self.tree.pack(pady=10)

    def add_training(self):
        date_str = self.date_entry.get().strip()
        t_type = self.type_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        # Проверка данных
        if not date_str or not t_type or not duration_str:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        # Проверка формата даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неправильный формат даты! Используйте гггг-мм-дд.")
            return

        # Проверка длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавление записи
        record = {
            "date": date_str,
            "type": t_type,
            "duration": int(duration_str)
        }
        self.data.append(record)
        self.save_data()
        self.load_data()
        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def load_data(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

        self.show_data(self.data)

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def show_data(self, data):
        self.tree.delete(*self.tree.get_children())
        for record in data:
            self.tree.insert("", tk.END, values=(record["date"], record["type"], record["duration"]))

    def apply_filter(self):
        filter_type = self.filter_type.get().strip().lower()
        filter_date = self.filter_date.get().strip()

        filtered = self.data
        if filter_type:
            filtered = [d for d in filtered if filter_type in d["type"].lower()]
        if filter_date:
            filtered = [d for d in filtered if d["date"] == filter_date]

        self.show_data(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
