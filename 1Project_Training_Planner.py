import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='x')

        # Дата
        ttk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky='w')
        self.date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.date_var).grid(row=0, column=1)

        # Тип тренировки
        ttk.Label(frame, text="Тип тренировки:").grid(row=1, column=0, sticky='w')
        self.type_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.type_var).grid(row=1, column=1)

        # Длительность
        ttk.Label(frame, text="Длительность (мин):").grid(row=2, column=0, sticky='w')
        self.duration_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.duration_var).grid(row=2, column=1)

        # Кнопка добавления
        ttk.Button(frame, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=5)

        # Фильтры
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky='w')
        self.filter_type_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_type_var).grid(row=0, column=1)
        ttk.Button(filter_frame, text="Фильтр", command=self.apply_filter).grid(row=0, column=2, padx=5)

        ttk.Label(filter_frame, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=1, column=0, sticky='w')
        self.filter_date_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_date_var).grid(row=1, column=1)
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=1, column=2, padx=5)

        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data).grid(row=2, column=1, pady=5)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность")
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Сохранение данных при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

    def add_training(self):
        date_str = self.date_var.get()
        t_type = self.type_var.get()
        duration_str = self.duration_var.get()

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")
            return

        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки")
            return

        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        # Добавление записи
        entry = {
            "date": date_str,
            "type": t_type,
            "duration": duration
        }
        self.data.append(entry)
        self.refresh_table()
        self.clear_inputs()

    def clear_inputs(self):
        self.date_var.set("")
        self.type_var.set("")
        self.duration_var.set("")

    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if data is None:
            data = self.data
        for item in data:
            self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def apply_filter(self):
        filtered_data = self.data
        filter_type = self.filter_type_var.get().strip()
        filter_date = self.filter_date_var.get().strip()

        if filter_type:
            filtered_data = [d for d in filtered_data if d["type"] == filter_type]
        if filter_date:
            try:
                datetime.strptime(filter_date, "%d.%m.%Y")
                filtered_data = [d for d in filtered_data if d["date"] == filter_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты фильтра")
                return

        self.refresh_table(filtered_data)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []
        self.refresh_table()

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def save_and_exit(self):
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
