import tkinter as tk
import random
class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, command=None, *args, **kwargs):
        self.bg_color = kwargs.pop('bg', 'black')
        super().__init__(parent, width=50, height=25, highlightthickness=0, bg=self.bg_color, *args, **kwargs)
        self.command = command
        self.is_on = False
        self.color_off = "#888888"
        self.color_on = "#00cc66"
        self.thumb_color = "#ffffff"
        self.bind("<Button-1>", self.toggle)
        self.draw()
    def update_bg(self, bg_color):
        self.config(bg=bg_color)
        self.bg_color = bg_color
        self.draw()
    def draw(self):
        self.delete("all")
        bg_fill = self.color_on if self.is_on else self.color_off
        self.create_oval(2, 2, 23, 23, fill=bg_fill, outline="")
        self.create_oval(27, 2, 48, 23, fill=bg_fill, outline="")
        self.create_rectangle(12, 2, 38, 23, fill=bg_fill, outline="")
        thumb_x = 37 if self.is_on else 13
        self.create_oval(thumb_x-9, 4, thumb_x+9, 21, fill=self.thumb_color, outline="")
    def toggle(self, event=None):
        self.is_on = not self.is_on
        self.draw()
        if self.command: self.command(self.is_on)
class OneTimeTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.shown = False
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.enter, add="+")
        self.widget.bind("<Leave>", self.leave, add="+")
        self.widget.bind("<ButtonPress>", self.leave, add="+")
    def enter(self, event=None):
        if self.shown: return
        self.shown = True
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0", foreground="black", relief='solid', borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=6, ipady=3)
    def leave(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
class BackgroundAnimation:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.words = ["csv", "html", "sqlite", "json"]
        self.items = []
        for _ in range(16):
            word = random.choice(self.words)
            x, y = random.randint(50, 700), random.randint(50, 500)
            dx, dy = random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5)
            if abs(dx) < 0.4: dx = 1.0 if dx > 0 else -1.0
            if abs(dy) < 0.4: dy = 1.0 if dy > 0 else -1.0
            font_size = random.randint(20, 70)
            item_id = self.canvas.create_text(x, y, text=word, font=('Courier New', font_size, 'bold')) 
            self.items.append({"id": item_id, "x": x, "y": y, "dx": dx, "dy": dy, "size": font_size})
    def update_colors(self, color):
        for item in self.items: self.canvas.itemconfig(item["id"], fill=color)
    def animate(self):
        width, height = self.root.winfo_width(), self.root.winfo_height()
        if width <= 1: width = 750
        if height <= 1: height = 550
        for item in self.items:
            item["x"] += item["dx"]
            item["y"] += item["dy"]
            bounds = item["size"] + 20
            if item["x"] < -bounds or item["x"] > width + bounds: item["dx"] *= -1
            if item["y"] < -bounds or item["y"] > height + bounds: item["dy"] *= -1
            self.canvas.coords(item["id"], item["x"], item["y"])
        self.root.after(35, self.animate)
