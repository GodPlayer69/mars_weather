import tkinter as tk
from tkinter import ttk

def apply_theme(style: ttk.Style, theme_name: str):
    """
    ttk için basit tema uygular.
    theme_name: "light" veya "dark"
    """
    try:
        style.theme_use("clam")  # ttk'de temel tema
    except:
        pass

    if theme_name == "dark":
        bg = "#1e1e1e"
        fg = "#e7e7e7"
        sbg = "#2a2a2a"
        style.configure(".", background=bg, foreground=fg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TFrame", background=bg)
        style.configure("TButton", background=sbg, foreground=fg, padding=6)
        style.configure("TCombobox", fieldbackground=sbg, background=sbg, foreground=fg)
        style.configure("TRadiobutton", background=bg, foreground=fg)
    else:
        # light tema, ttk default yeterli
        pass
