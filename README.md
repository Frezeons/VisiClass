# Öğrenci Yoklama Sistemi (Student Attendance System)

Bu proje, yüz tanıma teknolojisi kullanarak öğrenci yoklama almayı otomatikleştiren bir web uygulamasıdır.

## Özellikler

- 👤 Öğrenci kaydı (fotoğraf, ad-soyad, okul numarası)
- 📸 Kamera ile fotoğraf çekme veya dosyadan yükleme
- 🎯 Gerçek zamanlı yüz tanıma ile yoklama alma
- 📋 Öğrenci listesi görüntüleme ve yönetimi
- 🔍 Anlık yoklama durumu ve sonuç raporlama

## Kurulum

### Gereksinimler

- Python 3.8+
- pip (Python paket yöneticisi)
- Webcam (yoklama için)

### Adımlar

1. Virtual environment oluşturun ve aktif edin:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Gerekli paketleri yükleyin:
```powershell
pip install flask flask-sqlalchemy opencv-python
```

3. Yüz tanıma modellerini indirin:
```powershell
python download_face_models.py
```

4. Uygulamayı başlatın:
```powershell
python app.py
```

5. Tarayıcıda http://localhost:5000 adresine gidin

## Kullanım

### 1. Öğrenci Kaydı
- "Kayıt" sayfasından yeni öğrenci ekleyin
- Ad, soyad ve okul numarası girin
- Fotoğraf yükleyin veya kamera ile çekin

### 2. Yoklama Alma
- "Yoklama" sayfasını açın
- Kamera otomatik olarak aktif olur
- Tanınan öğrenciler sağ panelde listelenir
- "Yoklamayı Bitir" ile rapor alın

### 3. Öğrenci Listesi
- Tüm kayıtlı öğrencileri görüntüleyin
- Fotoğrafları ve bilgileri kontrol edin
- Gerekirse kayıtları silin

## Veritabanı

Varsayılan olarak `ogrenciler.db` SQLite veritabanı kullanılır. Konumunu değiştirmek için:

```powershell
$env:DATABASE_URL="sqlite:///yeni/konum/ogrenciler.db"
python app.py
```

## Proje Yapısı

```
.
├── app.py                 # Ana Flask uygulaması
├── static/
│   ├── style.css         # Özel CSS stilleri
│   ├── models/           # Yüz tanıma modelleri
│   └── ogrenci_fotolari/ # Öğrenci fotoğrafları
├── templates/            # Sayfa şablonları
│   ├── base.html        # Ana şablon
│   ├── index.html       # Ana sayfa
│   ├── kayit.html      # Öğrenci kayıt formu
│   ├── yoklama.html    # Yoklama sayfası
│   └── ...
└── README.md            # Bu dosya
```


# Student Attendance System

A web application that automates student attendance using face recognition technology.

## Features

- 👤 Student registration (photo, name, student ID)
- 📸 Camera capture or file upload for photos
- 🎯 Real-time face recognition for attendance
- 📋 Student list management
- 🔍 Live attendance status and reporting

## Setup

### Requirements

- Python 3.8+
- pip (Python package manager)
- Webcam (for attendance)

### Steps

1. Create and activate virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install required packages:
```powershell
pip install flask flask-sqlalchemy opencv-python
```

3. Download face recognition models:
```powershell
python download_face_models.py
```

4. Start the application:
```powershell
python app.py
```

5. Visit http://localhost:5000 in your browser

## Usage

### 1. Student Registration
- Add new students via the "Register" page
- Enter name and student ID
- Upload or capture a photo

### 2. Taking Attendance
- Open the "Attendance" page
- Camera activates automatically
- Recognized students appear in right panel
- Click "Finish Attendance" for report

### 3. Student List
- View all registered students
- Check photos and information
- Delete records if needed

## Database

Uses SQLite database `ogrenciler.db` by default. To change location:

```powershell
$env:DATABASE_URL="sqlite:///new/location/ogrenciler.db"
python app.py
```

## Project Structure

```
.
├── app.py                 # Main Flask application
├── static/
│   ├── style.css         # Custom CSS styles
│   ├── models/           # Face recognition models
│   └── ogrenci_fotolari/ # Student photos
├── templates/            # Page templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── kayit.html      # Student registration form
│   ├── yoklama.html    # Attendance page
│   └── ...
└── README.md            # This file
```
