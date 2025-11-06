from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import cv2
import os
from datetime import datetime
import shutil
import pathlib

# Allow changing DB file via environment variable DATABASE_URL, default to sqlite:///ogrenciler.db
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///ogrenciler.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Öğrenci modeli
class Ogrenci(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    okul_no = db.Column(db.String(20), unique=True, nullable=False)
    foto_path = db.Column(db.String(200))
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        # FormData üzerinden gönderilen ad, soyad, okul_no ve photo (file) beklenir
        ad = request.form.get('ad', '').strip()
        soyad = request.form.get('soyad', '').strip()
        okul_no = request.form.get('okul_no', '').strip()

        if not ad or not soyad or not okul_no:
            return jsonify({'success': False, 'error': 'Ad, soyad ve okul numarası gerekli.'})

        # Foto dosyasını al
        photo = request.files.get('photo')
        if not photo:
            return jsonify({'success': False, 'error': 'Fotoğraf yüklenmedi.'})

        # Fotoğraf klasörünü kontrol et/oluştur (static altında)
        foto_dir = os.path.join('static', 'ogrenci_fotolari')
        if not os.path.exists(foto_dir):
            os.makedirs(foto_dir)

        # Dosya adını okul_no ile eşleştir, uzantıyı koru
        from werkzeug.utils import secure_filename
        filename = secure_filename(photo.filename) if photo.filename else f"{okul_no}.jpg"
        _, ext = os.path.splitext(filename)
        if not ext:
            ext = '.jpg'
        target_filename = f"{okul_no}{ext}"
        file_path = os.path.join(foto_dir, target_filename)

        try:
            photo.save(file_path)
        except Exception as e:
            return jsonify({'success': False, 'error': f'Fotoğraf kaydedilemedi: {e}'})

        # DB kaydı
        ad_soyad = f"{ad} {soyad}"
        foto_path = f'ogrenci_fotolari/{target_filename}'
        yeni_ogrenci = Ogrenci(
            ad_soyad=ad_soyad,
            okul_no=okul_no,
            foto_path=foto_path
        )
        try:
            db.session.add(yeni_ogrenci)
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('ogrenci_listesi')})
        except Exception as e:
            db.session.rollback()
            # Eğer okul_no benzersizliği nedeniyle hata ise dosyayı sil
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
            # Duplicate error için özel mesaj
            if 'UNIQUE constraint failed' in str(e) and 'ogrenci.okul_no' in str(e):
                return jsonify({'success': False, 'error': 'Bu okul numarası ile zaten bir kayıt var. Lütfen farklı bir okul numarası girin.'})
            return jsonify({'success': False, 'error': 'Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.'})

    return render_template('kayit.html')

@app.route('/fotograf_cek/<okul_no>')
def fotograf_cek(okul_no):
    return render_template('fotograf_cek.html', okul_no=okul_no)

@app.route('/fotograf_kaydet', methods=['POST'])
def fotograf_kaydet():
    data = request.get_json()
    okul_no = data['okul_no']
    image_data = data['image_data']
    
    # Base64 görüntüyü kaydet (static/ogrenci_fotolari içine)
    import base64
    img_data = base64.b64decode(image_data.split(',')[1])
    foto_dir = os.path.join('static', 'ogrenci_fotolari')
    if not os.path.exists(foto_dir):
        os.makedirs(foto_dir)

    file_path = os.path.join(foto_dir, f"{okul_no}.jpg")
    with open(file_path, 'wb') as f:
        f.write(img_data)
    
    return jsonify({'success': True})

@app.route('/ogrenci_listesi')
def ogrenci_listesi():
    ogrenciler = Ogrenci.query.all()
    return render_template('ogrenci_listesi.html', ogrenciler=ogrenciler)


@app.route('/yoklama')
def yoklama():
    return render_template('yoklama.html')


@app.route('/api/known_faces')
def api_known_faces():
    ogrenciler = Ogrenci.query.all()
    # return list of {label, url}
    result = []
    for o in ogrenciler:
        label = f"{o.ad_soyad} ({o.okul_no})"
        # Ensure the photo file is inside static/ogrenci_fotolari
        static_path = os.path.join('static', o.foto_path)
        original_path = o.foto_path
        # If static file missing, check project-root 'ogrenci_fotolari/<file>' and copy it
        if not os.path.exists(static_path):
            possible_root = os.path.join('.', o.foto_path)
            if os.path.exists(possible_root):
                os.makedirs(os.path.dirname(static_path), exist_ok=True)
                try:
                    from shutil import copy2
                    copy2(possible_root, static_path)
                except Exception as e:
                    app.logger.warning(f"Could not copy {possible_root} to {static_path}: {e}")
        url = url_for('static', filename=o.foto_path)
        result.append({'label': label, 'okul_no': o.okul_no, 'url': url})
    return jsonify(result)


@app.route('/ogrenci_sil', methods=['POST'])
def ogrenci_sil():
    """Delete a student record by id (expects JSON {id: <id>}). Removes DB row and photo file if present."""
    data = request.get_json() or {}
    sid = data.get('id')
    if not sid:
        return jsonify({'success': False, 'error': 'ID belirtilmedi.'}), 400

    ogr = Ogrenci.query.get(sid)
    if not ogr:
        return jsonify({'success': False, 'error': 'Öğrenci bulunamadı.'}), 404

    # remove photo file if exists under static/
    try:
        static_path = os.path.join('static', ogr.foto_path) if ogr.foto_path else None
        if static_path and os.path.exists(static_path):
            os.remove(static_path)
    except Exception as e:
        app.logger.warning(f"Fotoğraf silinirken hata: {e}")

    try:
        db.session.delete(ogr)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Öğrenci silinirken hata: {e}")
        return jsonify({'success': False, 'error': 'Silme sırasında hata oluştu.'}), 500

if __name__ == '__main__':
    app.run(debug=True)