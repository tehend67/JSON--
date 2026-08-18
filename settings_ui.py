import tkinter as tk
from animations import ToggleSwitch
class SettingsPanel:
    def __init__(self, parent, on_theme_change, on_time_toggle, on_date_toggle, on_close):
        self.panel = tk.Frame(parent, width=280)
        self.visible = False
        self.settings_title = tk.Label(self.panel, text="Настройки", font=('Arial', 16, 'bold'))
        self.settings_title.pack(pady=20)
        f1 = tk.Frame(self.panel)
        f1.pack(fill="x", padx=20, pady=12)
        self.lbl_theme = tk.Label(f1, text="Светлая тема", font=('Arial', 11))
        self.lbl_theme.pack(side="left")
        self.switch_theme = ToggleSwitch(f1, command=on_theme_change)
        self.switch_theme.pack(side="right")
        f2 = tk.Frame(self.panel)
        f2.pack(fill="x", padx=20, pady=12)
        self.lbl_time = tk.Label(f2, text="Виджет времени", font=('Arial', 11))
        self.lbl_time.pack(side="left")
        self.switch_time = ToggleSwitch(f2, command=on_time_toggle)
        self.switch_time.pack(side="right")
        f3 = tk.Frame(self.panel)
        f3.pack(fill="x", padx=20, pady=12)
        self.lbl_date = tk.Label(f3, text="Виджет даты", font=('Arial', 11))
        self.lbl_date.pack(side="left")
        self.switch_date = ToggleSwitch(f3, command=on_date_toggle)
        self.switch_date.pack(side="right")
        self.close_btn = tk.Button(self.panel, text="Закрыть", command=on_close, relief=tk.FLAT, font=('Arial', 11, 'bold'), cursor="hand2")
        self.close_btn.pack(side="bottom", pady=25, padx=25, fill="x")
        self.bg_widgets = [f1, f2, f3]
        self.fg_bg_widgets = [self.settings_title, self.lbl_theme, self.lbl_time, self.lbl_date]
        self.switches = [self.switch_theme, self.switch_time, self.switch_date]
    def toggle(self):
        if self.visible:
            self.panel.place_forget()
            self.visible = False
        else:
            self.panel.place(relx=1.0, rely=0.0, relheight=1.0, anchor="ne")
            self.panel.lift()
            self.visible = True
    def apply_theme(self, theme):
        self.panel.config(bg=theme["panel_bg"], highlightbackground=theme["border"], highlightthickness=1)
        for w in self.bg_widgets: w.config(bg=theme["panel_bg"])
        for w in self.fg_bg_widgets: w.config(bg=theme["panel_bg"], fg=theme["fg"])
        self.close_btn.config(bg=theme["btn_bg"], fg=theme["fg"], activebackground=theme["btn_active"], activeforeground=theme["fg"])
        for sw in self.switches: sw.update_bg(theme["panel_bg"])
