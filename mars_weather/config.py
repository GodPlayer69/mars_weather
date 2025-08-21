# --- Configuration ---

# NASA API key (kendi keyini buraya yaz)
API_KEY = "YOUR_NASA_API_KEY"

# Auto-refresh interval in minutes (0 yaparsan kapalı olur)
AUTO_REFRESH_MINUTES = 30

# Kaç Sol geriye dönük grafik çizilsin
RECENT_SOLS_WINDOW = 7

# Uyarı eşikleri
# Ortalama sıcaklık (Celsius) bu değerin altına düşerse uyarı ver
TEMP_AVG_LOW_WARNING_C = -90.0

# NASA InSight API URL template
API_URL_TEMPLATE = "https://api.nasa.gov/insight_weather/?api_key={api_key}&feedtype=json&ver=1.0"
