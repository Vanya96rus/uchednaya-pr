import customtkinter as ctk
from tkinter import messagebox
from database import Database
from models import Product
from windows.workshops_window import WorkshopsWindow
from windows.calculator_window import CalculatorWindow
import os
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLORS = {
    "additional": "#D2DFFF",
    "accent": "#355CBD",
    "success": "#27AE60"
}

class MainWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Мебельная компания 'Комфорт'")
        self.window.geometry("950x650")
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 950) // 2
        y = (self.window.winfo_screenheight() - 650) // 2
        self.window.geometry(f'950x650+{x}+{y}')
        
        self.db = Database()
        self.selected_id = None
        
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        header_frame = ctk.CTkFrame(self.window, fg_color=COLORS["additional"], height=100, corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo.png")
            if os.path.exists(icon_path):
                pil_image = Image.open(icon_path)
                logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(60, 60))
                logo_label = ctk.CTkLabel(header_frame, image=logo_image, text="")
                logo_label.place(x=20, y=20)
            else:
                self.create_logo_fallback(header_frame)
        except:
            self.create_logo_fallback(header_frame)
        
        title_label = ctk.CTkLabel(header_frame, 
                                  text="МЕБЕЛЬНАЯ КОМПАНИЯ 'КОМФОРТ'", 
                                  font=("Arial", 24, "bold"), 
                                  text_color=COLORS["accent"])
        title_label.place(x=100, y=30)
        
        subtitle_label = ctk.CTkLabel(header_frame, 
                                      text="Управление продукцией и цехами", 
                                      font=("Arial", 14), 
                                      text_color="#666666")
        subtitle_label.place(x=100, y=60)
        
        btn_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        buttons = [
            ("➕ Добавить товар", self.add_product),
            ("✏️ Редактировать", self.edit_product),
            ("🏭 Управление цехами", self.show_workshops),
            ("🧮 Калькулятор", self.show_calculator),
            ("🔄 Обновить", self.refresh)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(btn_frame, text=text, width=140, height=35, 
                               fg_color=COLORS["accent"] if i == 0 else COLORS["additional"],
                               text_color="white" if i == 0 else "black",
                               command=cmd)
            btn.grid(row=0, column=i, padx=5)
        
        list_header = ctk.CTkFrame(self.window, fg_color=COLORS["additional"], height=30)
        list_header.pack(fill="x", padx=10, pady=(10,0))
        
        header_label = ctk.CTkLabel(list_header, 
                                    text="КАТАЛОГ ПРОДУКЦИИ", 
                                    text_color=COLORS["accent"])
        header_label.pack(pady=5)
        
        self.list_frame = ctk.CTkScrollableFrame(self.window, fg_color=COLORS["additional"])
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.status = ctk.CTkLabel(self.window, text="Готов к работе", anchor="w",
                                  fg_color=COLORS["additional"], height=30)
        self.status.pack(fill="x", padx=10, pady=5)
    
    def create_logo_fallback(self, parent_frame):
        logo_frame = ctk.CTkFrame(parent_frame, width=60, height=60, 
                                  fg_color=COLORS["accent"], corner_radius=30)
        logo_frame.place(x=20, y=20)
        
        logo_label = ctk.CTkLabel(logo_frame, text="К", font=("Arial", 30, "bold"), 
                                  text_color="white")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def load_products(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        rows = self.db.get_products()
        
        if not rows:
            ctk.CTkLabel(self.list_frame, text="Нет данных в базе").pack(pady=20)
            self.status.configure(text="Нет данных")
            return
        
        for row in rows:
            p = Product.from_db_row(row)
            self.create_product_card(p)
        
        self.status.configure(text=f"Загружено: {len(rows)} записей")
    
    def create_product_card(self, p):
        card = ctk.CTkFrame(self.list_frame, fg_color="white", 
                           border_width=1, border_color=COLORS["accent"])
        card.pack(fill="x", pady=2, padx=5)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        article_label = ctk.CTkLabel(info_frame, text=f"📦 Артикул: {p.article}", 
                                     font=("Arial", 10), text_color="#666666", anchor="w")
        article_label.pack(anchor="w")
        
        name_label = ctk.CTkLabel(info_frame, text=p.name, font=("Arial", 14, "bold"), 
                                  text_color=COLORS["accent"], anchor="w")
        name_label.pack(anchor="w")
        
        price_label = ctk.CTkLabel(info_frame, text=f"💰 {p.format_price()}", 
                                   font=("Arial", 12))
        price_label.pack(anchor="w")
        
        select_btn = ctk.CTkButton(card, text="Выбрать", width=80, height=30,
                                   fg_color=COLORS["success"],
                                   command=lambda pid=p.id: self.select_product(pid))
        select_btn.pack(side="right", padx=10, pady=10)
    
    def select_product(self, pid):
        self.selected_id = pid
        self.status.configure(text=f"Выбран продукт ID: {pid}")
    
    def add_product(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Добавление продукта")
        dialog.geometry("350x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 350) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 200) // 2
        dialog.geometry(f'350x200+{x}+{y}')
        
        ctk.CTkLabel(dialog, text="Название продукта:", font=("Arial", 12)).pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Цена (руб):", font=("Arial", 12)).pack(pady=5)
        price_entry = ctk.CTkEntry(dialog, width=250)
        price_entry.pack(pady=5)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название продукта")
                return
            
            try:
                price = float(price_entry.get())
                if price <= 0:
                    messagebox.showerror("Ошибка", "Цена должна быть положительной")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную цену")
                return
            
            pid, article = self.db.add_product(name, price)
            messagebox.showinfo("Успех", f"Продукт '{name}' добавлен!\nАртикул: {article}")
            dialog.destroy()
            self.load_products()
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="Сохранить", width=100, command=save).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Отмена", width=100, command=dialog.destroy).pack(side="left", padx=5)
    
    def edit_product(self):
        if not self.selected_id:
            messagebox.showwarning("Внимание", "Сначала выберите продукт")
            return
        
        row = self.db.get_product_by_id(self.selected_id)
        if not row:
            messagebox.showerror("Ошибка", "Продукт не найден")
            return
        
        p = Product.from_db_row(row)
        
        dialog = ctk.CTkToplevel(self.window)
        dialog.title(f"Редактирование продукта (Артикул: {p.article})")
        dialog.geometry("350x220")
        dialog.transient(self.window)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 350) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 220) // 2
        dialog.geometry(f'350x220+{x}+{y}')
        
        article_frame = ctk.CTkFrame(dialog, fg_color=COLORS["additional"], corner_radius=5)
        article_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(article_frame, text=f"Артикул: {p.article}", 
                    font=("Arial", 11, "bold")).pack(pady=3)
        
        ctk.CTkLabel(dialog, text="Название продукта:", font=("Arial", 12)).pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=5)
        name_entry.insert(0, p.name)
        
        ctk.CTkLabel(dialog, text="Цена (руб):", font=("Arial", 12)).pack(pady=5)
        price_entry = ctk.CTkEntry(dialog, width=250)
        price_entry.pack(pady=5)
        price_entry.insert(0, str(p.price))
        
        def update():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название продукта")
                return
            
            try:
                price = float(price_entry.get())
                if price <= 0:
                    messagebox.showerror("Ошибка", "Цена должна быть положительной")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную цену")
                return
            
            if self.db.update_product(p.id, name, price):
                messagebox.showinfo("Успех", f"Продукт '{name}' обновлен")
                dialog.destroy()
                self.load_products()
                self.selected_id = None
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить продукт")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="Обновить", width=100, command=update).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Отмена", width=100, command=dialog.destroy).pack(side="left", padx=5)
    
    def show_workshops(self):
        WorkshopsWindow(self.window, self.db)
    
    def show_calculator(self):
        CalculatorWindow(self.window)
    
    def refresh(self):
        self.load_products()
        self.status.configure(text="Список обновлен")
    
    def run(self):
        self.window.mainloop()