# Mars Weather App (Tkinter, NASA InSight)

Bu bir **masaüstü Python uygulamasıdır** ve Mars yüzeyindeki hava durumunu NASA InSight API'sinden çeker. HTML kullanmadan, tamamen Python/Tkinter ile yapılmıştır.

## Özellikler

- Tkinter + ttk GUI
- Sol seçimi (Martian day)
- Celsius / Fahrenheit toggle
- Son birkaç Sol için grafikler (sıcaklık, rüzgar, basınç)
- Otomatik yenileme (30 dk veya ayarlanabilir)
- JSON / CSV olarak veri export
- Düşük sıcaklık uyarısı (threshold ayarlanabilir)
- Light / Dark tema desteği

## Gereksinimler

- Python 3.9+
- Pip paketleri:
  - `requests`
  - `matplotlib`

```
pip install requests matplotlib
```

## Kurulum

1. Proje klasörünü bilgisayarınıza alın.
2. `config.py` dosyasını açın ve kendi NASA API key’inizi yazın:
```python
API_KEY = "YOUR_NASA_API_KEY"
```
3. Gerekli paketleri yükleyin:
```
pip install -r requirements.txt
```
4. Uygulamayı başlatın:
```
python app.py
```

## Dosya Yapısı

```
MarsWeatherApp/
├── app.py          # Ana giriş noktası
├── config.py       # Ayarlar (API key, refresh, threshold)
├── nasa_client.py  # NASA API’den veri çekme
├── ui.py           # Ana Tkinter arayüzü
├── charts.py       # Grafikler (matplotlib)
├── utils.py        # Yardımcı fonksiyonlar (C->F, export)
├── themes.py       # Light / Dark tema
├── requirements.txt
└── README.md
```

## Notlar

- NASA API bazen rate-limited olabilir. Eğer veri gelmezse bir süre bekleyin.
- Grafikler son birkaç Sol’u gösterecek şekilde ayarlanmıştır (`RECENT_SOLS_WINDOW`).
- Auto-refresh süresini `config.py` içinden değiştirebilirsiniz.
- Dark / Light temayı `themes.py` üzerinden ayarlayabilirsiniz.
