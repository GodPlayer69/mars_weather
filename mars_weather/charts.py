from typing import Dict, List
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import c_to_f

def show_charts(root, sols: List[str], data: Dict[str, Dict], unit: str = "C"):
    """
    Tkinter içinde matplotlib grafiklerini gösterir.
    sols: gösterilecek sol listesi (string listesi)
    data: NASA API verisi
    unit: "C" veya "F"
    """
    window = tk.Toplevel(root)
    window.title("Mars Weather Charts")

    fig = Figure(figsize=(7,5))
    ax_temp = fig.add_subplot(311)
    ax_wind = fig.add_subplot(312)
    ax_pres = fig.add_subplot(313)

    sols_sorted = sorted(sols, key=lambda x: int(x))

    # --- Sıcaklık grafiği ---
    t_av, t_min, t_max = [], [], []
    for sol in sols_sorted:
        s = data.get(sol, {})
        at = s.get("AT", {}) or {}
        for lst in [at.get("av"), at.get("mn"), at.get("mx")]:
            if lst is None:
                lst = 0
        av = at.get("av")
        mn = at.get("mn")
        mx = at.get("mx")
        if unit=="F":
            av = c_to_f(av) if av is not None else 0
            mn = c_to_f(mn) if mn is not None else 0
            mx = c_to_f(mx) if mx is not None else 0
        t_av.append(av)
        t_min.append(mn)
        t_max.append(mx)
    ax_temp.plot(sols_sorted, t_av, label="Avg Temp", marker="o")
    ax_temp.plot(sols_sorted, t_min, label="Min Temp", marker="x")
    ax_temp.plot(sols_sorted, t_max, label="Max Temp", marker="^")
    ax_temp.set_ylabel(f"Temp ({unit})")
    ax_temp.set_title("Mars Temperature per Sol")
    ax_temp.legend()
    ax_temp.grid(True)

    # --- Rüzgâr grafiği ---
    w_avg = []
    for sol in sols_sorted:
        s = data.get(sol, {})
        hws = s.get("HWS", {}) or {}
        val = hws.get("av")
        w_avg.append(val if val is not None else 0)
    ax_wind.plot(sols_sorted, w_avg, label="Wind Speed", color="green", marker="o")
    ax_wind.set_ylabel("Wind (m/s)")
    ax_wind.set_title("Average Wind Speed per Sol")
    ax_wind.grid(True)

    # --- Basınç grafiği ---
    p_avg = []
    for sol in sols_sorted:
        s = data.get(sol, {})
        pre = s.get("PRE", {}) or {}
        val = pre.get("av")
        p_avg.append(val if val is not None else 0)
    ax_pres.plot(sols_sorted, p_avg, label="Pressure", color="red", marker="o")
    ax_pres.set_ylabel("Pressure (Pa)")
    ax_pres.set_xlabel("Sol")
    ax_pres.set_title("Average Pressure per Sol")
    ax_pres.grid(True)

    # --- Canvas ---
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
