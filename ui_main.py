import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import datetime
from formats_config import FORMATS, EXT_MAP, THEMES
from animations import OneTimeTooltip, BackgroundAnimation
from settings_ui import SettingsPanel
from converter_core import convert_json_file
class JSONConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Converter PRO")
        self.root.geometry("750x550")
        self.theme_mode = "dark"
        self.show_time = False
        self.show_date = False
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.filepath = None
        self.setup_ui()
        self.apply_theme()
        self.bg_anim.animate()
        self.update_clock()
    def setup_ui(self):
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_anim = BackgroundAnimation(self.bg_canvas, self.root)
        self.info_frame = tk.Frame(self.root)
        self.info_frame.place(x=15, y=15)
        self.time_label = tk.Label(self.info_frame, text="", font=('Arial', 14, 'bold'))
        self.date_label = tk.Label(self.info_frame, text="", font=('Arial', 10))
        self.settings_btn = tk.Button(self.root, text="⚙ Настройки", command=self.toggle_settings, font=('Arial', 10), relief=tk.FLAT, cursor="hand2")
        self.settings_btn.place(relx=1.0, x=-15, y=15, anchor="ne")
        OneTimeTooltip(self.settings_btn, "Здесь можно сменить тему\nи включить виджеты даты и времени")
        self.center_frame = tk.Frame(self.root, padx=20, pady=20, highlightthickness=1)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.title_label = tk.Label(self.center_frame, text="JSON Converter", font=('Arial', 26, 'bold'))
        self.title_label.pack(pady=10)
        self.select_btn = tk.Button(self.center_frame, text="Выбрать JSON файл", command=self.select_file, font=('Arial', 12, 'bold'), relief=tk.FLAT, padx=25, pady=12, cursor="hand2")
        self.select_btn.pack(pady=10)
        OneTimeTooltip(self.select_btn, "Нажмите, чтобы выбрать файл .json")
        self.file_label = tk.Label(self.center_frame, text="Файл не выбран", font=('Arial', 10))
        self.file_label.pack(pady=5)
        self.format_frame = tk.Frame(self.center_frame)
        self.format_label = tk.Label(self.format_frame, text="Выберите формат для конвертации:", font=('Arial', 12))
        self.format_label.pack(pady=10)
        self.format_var = tk.StringVar()
        self.format_combo = ttk.Combobox(self.format_frame, textvariable=self.format_var, values=FORMATS, state="readonly", font=('Arial', 12))
        self.format_combo.pack(pady=10)
        if FORMATS: self.format_combo.current(0)
        OneTimeTooltip(self.format_combo, "Выберите, в какой формат перевести данные")
        self.convert_btn = tk.Button(self.format_frame, text="Конвертировать", command=self.convert_file, font=('Arial', 12, 'bold'), relief=tk.FLAT, padx=30, pady=12, cursor="hand2")
        self.convert_btn.pack(pady=20)
        OneTimeTooltip(self.convert_btn, "Запустить процесс конвертации")
        self.settings_panel = SettingsPanel(self.root, self.change_theme, self.toggle_time_widget, self.toggle_date_widget, self.toggle_settings)
        self.bg_widgets = [self.root, self.info_frame, self.format_frame]
        self.fg_bg_widgets = [self.title_label, self.format_label, self.time_label, self.date_label]
    def apply_theme(self):
        t = THEMES[self.theme_mode]
        self.bg_canvas.config(bg=t["bg"])
        self.bg_anim.update_colors(t["anim_text"])
        for w in self.bg_widgets: w.config(bg=t["bg"])
        self.center_frame.config(bg=t["bg"], highlightbackground=t["border"])
        for w in self.fg_bg_widgets: w.config(bg=t["bg"], fg=t["fg"])
        self.file_label.config(bg=t["bg"], fg=t["success"] if self.filepath else t["muted"])
        self.select_btn.config(bg=t["btn_bg"], fg=t["fg"], activebackground=t["btn_active"], activeforeground=t["fg"])
        self.settings_btn.config(bg=t["btn_bg"], fg=t["fg"], activebackground=t["btn_active"], activeforeground=t["fg"])
        self.convert_btn.config(bg=t["accent"], fg="white", activebackground=t["accent_active"], activeforeground="white")
        self.style.configure('TCombobox', fieldbackground=t["btn_bg"], background=t["btn_bg"], foreground=t["fg"], borderwidth=0)
        self.style.map('TCombobox', fieldbackground=[('readonly', t["btn_bg"])], selectbackground=[('readonly', t["accent"])])
        self.settings_panel.apply_theme(t)
    def change_theme(self, is_light):
        self.theme_mode = "light" if is_light else "dark"
        self.apply_theme()
    def toggle_settings(self):
        self.settings_panel.toggle()
    def toggle_time_widget(self, is_on):
        self.show_time = is_on
        if is_on: self.time_label.pack(anchor="w")
        else: self.time_label.pack_forget()
        self.update_clock()
    def toggle_date_widget(self, is_on):
        self.show_date = is_on
        if is_on: self.date_label.pack(anchor="w")
        else: self.date_label.pack_forget()
        self.update_clock()
    def update_clock(self):
        now = datetime.datetime.now()
        if self.show_time: self.time_label.config(text=now.strftime("%H:%M:%S"))
        if self.show_date: self.date_label.config(text=now.strftime("%d.%m.%Y"))
    def _clock_loop(self):
        self.update_clock()
        self.root.after(1000, self._clock_loop)
    def select_file(self):
        self.filepath = filedialog.askopenfilename(title="Выберите файл", filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if self.filepath:
            self.file_label.config(text=f"Выбран файл: {os.path.basename(self.filepath)}", fg=THEMES[self.theme_mode]["success"])
            self.format_frame.pack(pady=10)
    def convert_file(self):
        if not self.filepath: return messagebox.showerror("Ошибка", "Сначала выберите файл.")
        if not self.format_var.get(): return messagebox.showerror("Ошибка", "Выберите формат.")
        fmt = self.format_var.get()
        ext = EXT_MAP.get(fmt, ".txt")
        save_path = filedialog.asksaveasfilename(defaultextension=ext, initialfile=os.path.splitext(os.path.basename(self.filepath))[0] + ext, title="Сохранить как", filetypes=[(f"{fmt} files", f"*{ext}"), ("All files", "*.*")])
        if not save_path: return
        try:
            self.convert_btn.config(text="Обработка...", state=tk.DISABLED)
            self.root.update()
            convert_json_file(self.filepath, save_path, fmt)
            messagebox.showinfo("Успех", f"Файл сохранен как:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось конвертировать:\n{e}")
        finally:
            self.convert_btn.config(text="Конвертировать", state=tk.NORMAL)
