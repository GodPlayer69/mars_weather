import tkinter as tk
from tkinter import ttk
from ui import MarsWeatherUI
from themes import apply_theme

def main():
    root = tk.Tk()
    root.title("🌌 Mars Weather App (NASA InSight)")
    root.geometry("700x600")

    style = ttk.Style()
    apply_theme(style, "light")  # "light" veya "dark" seçilebilir

    app = MarsWeatherUI(root)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
