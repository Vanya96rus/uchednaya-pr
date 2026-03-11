import customtkinter as ctk
from tkinter import messagebox
from models import Workshop

COLORS = {
    "additional": "#D2DFFF",
    "accent": "#355CBD",
    "success": "#27AE60"
}

class WorkshopsWindow:
    def __init__(self, parent, db):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Управление цехами")
        self.window.geometry("800x650")
        
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 800) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.window.geometry(f'800x650+{x}+{y}')
        
        self.db = db
        self.selected_id = None
        self.setup_ui()
        self.load_workshops()
    
    def setup_ui(self):
        title_frame = ctk.CTkFrame(self.window, fg_color=COLORS["accent"], corner_radius=10, height=60)
        title_frame.pack(fill="x", padx=20, pady=20)
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(title_frame, 
                                   text="🏭 УПРАВЛЕНИЕ ЦЕХАМИ", 
                                   font=("Arial", 20, "bold"), 
                                   text_color="white")
        title_label.pack(expand=True)
        
        control_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        control_frame.pack(pady=10)
        
        ctk.CTkButton(control_frame, text="➕ Добавить цех", width=150, height=35,
                     fg_color=COLORS["accent"], text_color="white",
                     command=self.add_workshop).pack(side="left", padx=5)
        
        ctk.CTkButton(control_frame, text="✏️ Редактировать", width=150, height=35,
                     fg_color=COLORS["additional"], text_color="black",
                     command=self.edit_workshop).pack(side="left", padx=5)
        
        ctk.CTkButton(control_frame, text="🗑️ Удалить", width=150, height=35,
                     fg_color="#FF6B6B", text_color="white",
                     command=self.delete_workshop).pack(side="left", padx=5)
        
        list_header = ctk.CTkFrame(self.window, fg_color=COLORS["additional"], height=30)
        list_header.pack(fill="x", padx=20, pady=(10,0))
        
        ctk.CTkLabel(list_header, text="СПИСОК ЦЕХОВ", 
                    text_color=COLORS["accent"]).pack(pady=5)
        
        self.list_frame = ctk.CTkScrollableFrame(self.window, fg_color=COLORS["additional"])
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        close_btn = ctk.CTkButton(self.window, 
                                  text="Закрыть", 
                                  width=120, 
                                  height=35,
                                  fg_color=COLORS["additional"], 
                                  text_color="black",
                                  command=self.window.destroy)
        close_btn.pack(pady=10)
    
    def load_workshops(self):
        self.selected_id = None
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        rows = self.db.get_workshops()
        
        for row in rows:
            w = Workshop.from_db_row(row)
            self.create_workshop_card(w)
    
    def create_workshop_card(self, w):
        card = ctk.CTkFrame(self.list_frame, fg_color="white", border_width=2, 
                           border_color=COLORS["accent"], corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)
        
        card.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=15)
        
        name_label = ctk.CTkLabel(container, 
                                  text=w.name, 
                                  font=("Arial", 18, "bold"), 
                                  text_color=COLORS["accent"])
        name_label.pack(anchor="w")
        name_label.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        stats_frame = ctk.CTkFrame(container, fg_color="transparent")
        stats_frame.pack(anchor="w", pady=8)
        stats_frame.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        emp_frame = ctk.CTkFrame(stats_frame, fg_color=COLORS["accent"], corner_radius=5)
        emp_frame.pack(side="left", padx=5)
        emp_frame.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        emp_label = ctk.CTkLabel(emp_frame, 
                                 text=f"👥 {w.employees} человек", 
                                 font=("Arial", 13, "bold"),
                                 text_color="white")
        emp_label.pack(padx=12, pady=5)
        emp_label.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        time_frame = ctk.CTkFrame(stats_frame, fg_color=COLORS["success"], corner_radius=5)
        time_frame.pack(side="left", padx=5)
        time_frame.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        time_label = ctk.CTkLabel(time_frame, 
                                  text=f"⏱️ {w.days} дней", 
                                  font=("Arial", 13, "bold"),
                                  text_color="white")
        time_label.pack(padx=12, pady=5)
        time_label.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
        
        if w.description:
            desc_label = ctk.CTkLabel(container, 
                                      text=w.description, 
                                      font=("Arial", 12),
                                      text_color="#333333", 
                                      wraplength=600, 
                                      justify="left")
            desc_label.pack(anchor="w", pady=5)
            desc_label.bind("<Button-1>", lambda e, wid=w.id: self.select_workshop(wid, card))
    
    def select_workshop(self, wid, card):
        for child in self.list_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.configure(border_color=COLORS["accent"], border_width=2)
        
        card.configure(border_color=COLORS["success"], border_width=3)
        self.selected_id = wid
    
    def add_workshop(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Добавление цеха")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 400) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 350) // 2
        dialog.geometry(f'400x350+{x}+{y}')
        
        ctk.CTkLabel(dialog, text="➕ НОВЫЙ ЦЕХ", font=("Arial", 16, "bold"), 
                    text_color=COLORS["accent"]).pack(pady=10)
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(pady=10)
        
        ctk.CTkLabel(frame, text="Название цеха:", font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        name_entry = ctk.CTkEntry(frame, width=200)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(frame, text="Описание:", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=5, sticky="w")
        desc_entry = ctk.CTkEntry(frame, width=200)
        desc_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ctk.CTkLabel(frame, text="Кол-во человек:", font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="w")
        emp_entry = ctk.CTkEntry(frame, width=200)
        emp_entry.grid(row=2, column=1, pady=5, padx=5)
        emp_entry.insert(0, "10")
        
        ctk.CTkLabel(frame, text="Время (дни):", font=("Arial", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="w")
        days_entry = ctk.CTkEntry(frame, width=200)
        days_entry.grid(row=3, column=1, pady=5, padx=5)
        days_entry.insert(0, "3")
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название цеха")
                return
            
            try:
                emp = int(emp_entry.get())
                if emp <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Количество человек должно быть положительным числом")
                return
            
            try:
                days = int(days_entry.get())
                if days <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Время должно быть положительным числом")
                return
            
            desc = desc_entry.get().strip()
            
            wid = self.db.add_workshop(name, desc, emp, days)
            if wid:
                messagebox.showinfo("Успех", f"Цех '{name}' добавлен")
                dialog.destroy()
                self.load_workshops()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить цех")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="Сохранить", width=100, command=save).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Отмена", width=100, command=dialog.destroy).pack(side="left", padx=5)
    
    def edit_workshop(self):
        if not self.selected_id:
            messagebox.showwarning("Внимание", "Сначала выберите цех")
            return
        
        row = self.db.get_workshop_by_id(self.selected_id)
        if not row:
            messagebox.showerror("Ошибка", "Цех не найден")
            return
        
        w = Workshop.from_db_row(row)
        
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Редактирование цеха")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 400) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 350) // 2
        dialog.geometry(f'400x350+{x}+{y}')
        
        ctk.CTkLabel(dialog, text="✏️ РЕДАКТИРОВАНИЕ ЦЕХА", font=("Arial", 16, "bold"), 
                    text_color=COLORS["accent"]).pack(pady=10)
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(pady=10)
        
        ctk.CTkLabel(frame, text="Название цеха:", font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=5, sticky="w")
        name_entry = ctk.CTkEntry(frame, width=200)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        name_entry.insert(0, w.name)
        
        ctk.CTkLabel(frame, text="Описание:", font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=5, sticky="w")
        desc_entry = ctk.CTkEntry(frame, width=200)
        desc_entry.grid(row=1, column=1, pady=5, padx=5)
        desc_entry.insert(0, w.description)
        
        ctk.CTkLabel(frame, text="Кол-во человек:", font=("Arial", 12)).grid(row=2, column=0, pady=5, padx=5, sticky="w")
        emp_entry = ctk.CTkEntry(frame, width=200)
        emp_entry.grid(row=2, column=1, pady=5, padx=5)
        emp_entry.insert(0, str(w.employees))
        
        ctk.CTkLabel(frame, text="Время (дни):", font=("Arial", 12)).grid(row=3, column=0, pady=5, padx=5, sticky="w")
        days_entry = ctk.CTkEntry(frame, width=200)
        days_entry.grid(row=3, column=1, pady=5, padx=5)
        days_entry.insert(0, str(w.days))
        
        def update():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название цеха")
                return
            
            try:
                emp = int(emp_entry.get())
                if emp <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Количество человек должно быть положительным числом")
                return
            
            try:
                days = int(days_entry.get())
                if days <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Время должно быть положительным числом")
                return
            
            desc = desc_entry.get().strip()
            
            if self.db.update_workshop(w.id, name, desc, emp, days):
                messagebox.showinfo("Успех", f"Цех '{name}' обновлен")
                dialog.destroy()
                self.load_workshops()
                self.selected_id = None
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить цех")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="Обновить", width=100, command=update).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Отмена", width=100, command=dialog.destroy).pack(side="left", padx=5)
    
    def delete_workshop(self):
        if not self.selected_id:
            messagebox.showwarning("Внимание", "Сначала выберите цех")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот цех?"):
            if self.db.delete_workshop(self.selected_id):
                messagebox.showinfo("Успех", "Цех удален")
                self.load_workshops()
                self.selected_id = None
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить цех")