import customtkinter as ctk
from tkinter import messagebox
from calculator import Calculator
import random

COLORS = {
    "additional": "#D2DFFF",
    "accent": "#355CBD",
    "success": "#27AE60"
}

class CalculatorWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Калькулятор сырья")
        self.window.geometry("550x650")
        
        self.window.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 550) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 650) // 2
        self.window.geometry(f'550x650+{x}+{y}')
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = ctk.CTkFrame(self.window, fg_color=COLORS["accent"], corner_radius=10, height=60)
        title_frame.pack(fill="x", padx=20, pady=20)
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(title_frame, 
                                   text="🧮 КАЛЬКУЛЯТОР РАСЧЕТА СЫРЬЯ", 
                                   font=("Arial", 20, "bold"), 
                                   text_color="white")
        title_label.pack(expand=True)
        
        form = ctk.CTkFrame(self.window, fg_color="transparent")
        form.pack(padx=30, pady=10, fill="both", expand=True)
        
        material_label = ctk.CTkLabel(form, 
                                     text="1. Выберите материал:", 
                                     font=("Arial", 14, "bold"),
                                     text_color=COLORS["accent"])
        material_label.pack(anchor="w", pady=(10, 5))
        
        self.material_combo = ctk.CTkComboBox(form, 
                                             values=Calculator.get_material_types(),
                                             width=400, 
                                             font=("Arial", 12),
                                             state="readonly")
        self.material_combo.pack(pady=5)
        self.material_combo.set("Дуб")
        
        product_label = ctk.CTkLabel(form, 
                                     text="2. Выберите тип изделия:", 
                                     font=("Arial", 14, "bold"),
                                     text_color=COLORS["accent"])
        product_label.pack(anchor="w", pady=(15, 5))
        
        self.product_combo = ctk.CTkComboBox(form, 
                                            values=Calculator.get_product_types(),
                                            width=400, 
                                            font=("Arial", 12),
                                            state="readonly")
        self.product_combo.pack(pady=5)
        self.product_combo.set("Стол")
        
        separator = ctk.CTkFrame(form, height=2, fg_color=COLORS["additional"])
        separator.pack(fill="x", pady=20)
        
        size_label = ctk.CTkLabel(form, 
                                  text="3. Введите размеры (в метрах):", 
                                  font=("Arial", 14, "bold"),
                                  text_color=COLORS["accent"])
        size_label.pack(anchor="w", pady=(0, 10))
        
        len_frame = ctk.CTkFrame(form, fg_color="transparent")
        len_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(len_frame, text="Длина:", font=("Arial", 12), width=80).pack(side="left")
        self.len_entry = ctk.CTkEntry(len_frame, width=150, placeholder_text="1.0")
        self.len_entry.pack(side="left", padx=10)
        self.len_entry.insert(0, "1.0")
        ctk.CTkLabel(len_frame, text="м", font=("Arial", 12)).pack(side="left")
        
        width_frame = ctk.CTkFrame(form, fg_color="transparent")
        width_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(width_frame, text="Ширина:", font=("Arial", 12), width=80).pack(side="left")
        self.width_entry = ctk.CTkEntry(width_frame, width=150, placeholder_text="0.5")
        self.width_entry.pack(side="left", padx=10)
        self.width_entry.insert(0, "0.5")
        ctk.CTkLabel(width_frame, text="м", font=("Arial", 12)).pack(side="left")
        
        height_frame = ctk.CTkFrame(form, fg_color="transparent")
        height_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(height_frame, text="Высота:", font=("Arial", 12), width=80).pack(side="left")
        self.height_entry = ctk.CTkEntry(height_frame, width=150, placeholder_text="0.1")
        self.height_entry.pack(side="left", padx=10)
        self.height_entry.insert(0, "0.1")
        ctk.CTkLabel(height_frame, text="м", font=("Arial", 12)).pack(side="left")
        
        qty_label = ctk.CTkLabel(form, 
                                 text="4. Количество изделий:", 
                                 font=("Arial", 14, "bold"),
                                 text_color=COLORS["accent"])
        qty_label.pack(anchor="w", pady=(15, 5))
        
        qty_frame = ctk.CTkFrame(form, fg_color="transparent")
        qty_frame.pack(fill="x")
        
        self.qty_entry = ctk.CTkEntry(qty_frame, width=150, placeholder_text="1")
        self.qty_entry.pack(side="left")
        self.qty_entry.insert(0, "1")
        ctk.CTkLabel(qty_frame, text="шт", font=("Arial", 12)).pack(side="left", padx=10)
        
        calc_btn = ctk.CTkButton(form, 
                                 text="🧮 РАССЧИТАТЬ", 
                                 width=300, 
                                 height=50,
                                 font=("Arial", 16, "bold"), 
                                 fg_color=COLORS["success"],
                                 hover_color="#219a52",
                                 command=self.calculate)
        calc_btn.pack(pady=25)
        
        result_frame = ctk.CTkFrame(form, fg_color=COLORS["accent"], corner_radius=10, height=80)
        result_frame.pack(fill="x", pady=10)
        result_frame.pack_propagate(False)
        
        self.result_label = ctk.CTkLabel(result_frame, 
                                         text="0 ед.", 
                                         font=("Arial", 32, "bold"), 
                                         text_color="white")
        self.result_label.pack(expand=True)
        
        note_label = ctk.CTkLabel(form, 
                                  text="* Учитываются коэффициенты материала и изделия, а также процент потерь",
                                  font=("Arial", 10),
                                  text_color="gray")
        note_label.pack(pady=5)
        
        close_btn = ctk.CTkButton(form, 
                                  text="Закрыть", 
                                  width=120, 
                                  height=35,
                                  font=("Arial", 12), 
                                  fg_color=COLORS["additional"],
                                  text_color="black",
                                  command=self.window.destroy)
        close_btn.pack(pady=10)
    
    def calculate(self):
        try:
            material = self.material_combo.get()
            product = self.product_combo.get()
            
            try:
                qty = int(self.qty_entry.get())
                if qty <= 0:
                    qty = 1
            except:
                messagebox.showerror("Ошибка", "Количество должно быть числом")
                return
            
            try:
                length = float(self.len_entry.get())
                if length <= 0:
                    length = 1.0
            except:
                messagebox.showerror("Ошибка", "Длина должна быть числом")
                return
            
            try:
                width = float(self.width_entry.get())
                if width <= 0:
                    width = 0.5
            except:
                messagebox.showerror("Ошибка", "Ширина должна быть числом")
                return
            
            try:
                height = float(self.height_entry.get())
                if height <= 0:
                    height = 0.1
            except:
                messagebox.showerror("Ошибка", "Высота должна быть числом")
                return
            
            result = Calculator.calculate(product, material, qty, length, width, height)
            
            if result == -1:
                self.result_label.configure(text="Ошибка")
                messagebox.showerror("Ошибка", "Не удалось рассчитать")
            else:
                self.result_label.configure(text=f"{result} ед.")
                messagebox.showinfo("Результат", 
                                   f"✅ РАСЧЕТ ВЫПОЛНЕН\n\n"
                                   f"Материал: {material}\n"
                                   f"Изделие: {product}\n"
                                   f"Количество: {qty} шт\n"
                                   f"Размеры: {length}м x {width}м x {height}м\n"
                                   f"Необходимо сырья: {result} ед.")
                
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))