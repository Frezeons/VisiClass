# VisiClass

> Kamera ve yüz tanımayla öğrenci yoklamasını otomatikleştiren web uygulaması.

**Durum:** okul projesi · **Stack:** Python · Flask · Flask-SQLAlchemy · OpenCV · SQLite

## Ne yapar
- Öğrenci kaydı: ad-soyad, okul numarası, fotoğraf (kameradan çekim veya dosya yükleme)
- Gerçek zamanlı yüz tanımayla yoklama; tanınan öğrenciler yan panelde listelenir
- "Yoklamayı Bitir" ile yoklama raporu
- Kayıtlı öğrenci listesi: görüntüleme ve silme

## Dizin yapısı
```
app.py                      # Flask uygulaması
templates/                  # base, index, kayit, yoklama ...
static/models/              # yüz tanıma modelleri
static/ogrenci_fotolari/    # öğrenci fotoğrafları
```

## Çalıştırma
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install flask flask-sqlalchemy opencv-python
python download_face_models.py   # yüz tanıma modellerini indirir
python app.py                    # http://localhost:5000
```

## Notlar
- Python 3.8+ ve webcam gerekir.
- Varsayılan veritabanı `ogrenciler.db`; konum `DATABASE_URL` ile değiştirilir (ör. `$env:DATABASE_URL="sqlite:///yeni/konum/ogrenciler.db"`).
