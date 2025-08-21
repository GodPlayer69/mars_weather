import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from nasa_client import NasaClient
from utils import c_to_f, export_json, export_csv
from charts import show_charts
from config import AUTO_REFRESH_MINUTES, TEMP_AVG_LOW_WARNING_C, RECENT_SOLS_WINDOW
import threading

class MarsWeatherUI(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=15)
        self.client = NasaClient()
        self.data_cache = {}
        self.create_widgets()
        self.fetch_data()
        # Auto refresh
        if AUTO_REFRESH_MINUTES > 0:
            self.after(AUTO_REFRESH_MINUTES*60*1000, self.auto_refresh)

    def create_widgets(self):
        # Başlık
        title = ttk.Label(self, text="🌌 Mars Weather App (InSight)", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,10))

        # Sol seçimi
        ttk.Label(self, text="Sol:").grid(row=1, column=0, sticky="e")
        self.sol_combo = ttk.Combobox(self, state="readonly", width=10)
        self.sol_combo.grid(row=1, column=1, sticky="w")
        self.sol_combo.bind("<<ComboboxSelected>>", self.on_sol_change)

        # Birim toggle
        self.unit_var = tk.StringVar(value="C")
        ttk.Radiobutton(self, text="Celsius", value="C", variable=self.unit_var, command=self.on_unit_change).grid(row=1, column=2)
        ttk.Radiobutton(self, text="Fahrenheit", value="F", variable=self.unit_var, command=self.on_unit_change).grid(row=1, column=3)

        # Butonlar
        self.refresh_btn = ttk.Button(self, text="Refresh", command=self.fetch_data)
        self.refresh_btn.grid(row=2, column=0, pady=8)
        self.export_btn = ttk.Button(self, text="Export", command=self.export_data)
        self.export_btn.grid(row=2, column=1, pady=8)
        self.chart_btn = ttk.Button(self, text="Charts", command=self.show_charts)
        self.chart_btn.grid(row=2, column=2, pady=8)

        # Sonuç alanı
        self.result_var = tk.StringVar(value="Fetching data...")
        self.result_label = ttk.Label(self, textvariable=self.result_var, justify="left", font=("Segoe UI", 11))
        self.result_label.grid(row=3, column=0, columnspan=4, sticky="w", pady=(12,0))

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        self.status = ttk.Label(self, textvariable=self.status_var, anchor="w", padding=6, relief="groove")
        self.status.grid(row=4, column=0, columnspan=4, sticky="we", pady=(10,0))

    def fetch_data(self):
        def thread_func():
            try:
                self.status_var.set("Fetching data from NASA...")
                self.data_cache = self.client.fetch()
                sol_keys = self.data_cache.get("sol_keys", [])
                if not sol_keys:
                    self.result_var.set("No Sol data available.")
                    self.status_var.set("API may be rate-limited.")
                    return
                sols_sorted = sorted(sol_keys, key=lambda x:int(x), reverse=True)
                self.sol_combo["values"] = sols_sorted
                self.sol_combo.current(0)
                self.show_sol(sols_sorted[0])
                self.status_var.set(f"Loaded {len(sols_sorted)} Sols.")
            except Exception as e:
                self.status_var.set("Error fetching data.")
                self.result_var.set(str(e))
        threading.Thread(target=thread_func, daemon=True).start()

    def show_sol(self, sol):
        s = self.data_cache.get(sol, {})
        at = s.get("AT", {}) or {}
        hws = s.get("HWS", {}) or {}
        pre = s.get("PRE", {}) or {}
        season = s.get("Season", "Unknown")
        first_utc = s.get("First_UTC", "")
        last_utc = s.get("Last_UTC", "")

        def fmt_temp(v):
            if v is None:
                return "N/A"
            return f"{v:.1f} °C" if self.unit_var.get()=="C" else f"{c_to_f(v):.1f} °F"

        t_min = fmt_temp(at.get("mn"))
        t_max = fmt_temp(at.get("mx"))
        t_avg = fmt_temp(at.get("av"))
        w_avg = f"{hws.get('av', 'N/A'):.1f} m/s" if hws.get("av") is not None else "N/A"
        p_avg = f"{pre.get('av', 'N/A'):.1f} Pa" if pre.get("av") is not None else "N/A"

        lines = [
            f"Mars Sol: {sol}",
            f"First UTC: {first_utc}",
            f"Last UTC:  {last_utc}",
            f"Season: {season}",
            "",
            f"Temperature Avg: {t_avg}",
            f"Temperature Min: {t_min}",
            f"Temperature Max: {t_max}",
            f"Wind Speed Avg: {w_avg}",
            f"Pressure Avg: {p_avg}"
        ]
        self.result_var.set("\n".join(lines))

        # Bildirim
        try:
            if at.get("av") is not None and at.get("av") < TEMP_AVG_LOW_WARNING_C:
                messagebox.showwarning("Low Temp Warning", f"Average temp {at.get('av')}°C is below threshold!")
        except:
            pass

    def on_sol_change(self, event=None):
        sel = self.sol_combo.get()
        if sel:
            self.show_sol(sel)

    def on_unit_change(self):
        sel = self.sol_combo.get()
        if sel:
            self.show_sol(sel)

    def export_data(self):
        sols = self.sol_combo["values"]
        if not sols:
            messagebox.showinfo("Export", "No data to export.")
            return
        filetypes = [("JSON", "*.json"), ("CSV", "*.csv")]
        filepath = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".json")
        if not filepath:
            return
        try:
            if filepath.endswith(".json"):
                export_json(filepath, self.data_cache)
            else:
                export_csv(filepath, sols, self.data_cache)
            messagebox.showinfo("Export", f"Data saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def show_charts(self):
        sols = self.sol_combo["values"]
        if not sols:
            messagebox.showinfo("Charts", "No data to show.")
            return
        show_charts(self.master, list(sols)[-RECENT_SOLS_WINDOW:], self.data_cache, self.unit_var.get())

    def auto_refresh(self):
        self.fetch_data()
        # tekrar planla
        if AUTO_REFRESH_MINUTES > 0:
            self.after(AUTO_REFRESH_MINUTES*60*1000, self.auto_refresh)
