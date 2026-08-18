import tkinter as tk
from ui_main import JSONConverterApp
if __name__ == "__main__":
    root = tk.Tk()
    app = JSONConverterApp(root)
    app._clock_loop()
    root.mainloop()
