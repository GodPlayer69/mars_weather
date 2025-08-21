from datetime import datetime
import csv
import json

# --- Sıcaklık dönüşümü ---
def c_to_f(c):
    return (c * 9.0 / 5.0) + 32.0

# --- UTC tarih formatlama ---
def format_utc(dt_str):
    if not dt_str:
        return ""
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return dt_str

# --- JSON export ---
def export_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- CSV export ---
def export_csv(filepath, sols, data):
    """
    Sol başına sıcaklık, rüzgar, basınç gibi bilgileri CSV'ye kaydeder.
    """
    headers = ["sol","first_utc","last_utc","season","temp_av","temp_mn","temp_mx","wind_av","pressure_av"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for sol in sols:
            s = data.get(sol, {})
            at = s.get("AT", {}) or {}
            hws = s.get("HWS", {}) or {}
            pre = s.get("PRE", {}) or {}
            row = [
                sol,
                s.get("First_UTC", ""),
                s.get("Last_UTC", ""),
                s.get("Season", ""),
                safe_num(at.get("av")),
                safe_num(at.get("mn")),
                safe_num(at.get("mx")),
                safe_num(hws.get("av")),
                safe_num(pre.get("av")),
            ]
            writer.writerow(row)

def safe_num(v):
    try:
        if v is None:
            return ""
        return float(v)
    except Exception:
        return ""
