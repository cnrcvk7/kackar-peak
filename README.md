# Kaçkar Peak

Koşu, yoga ve doğa yürüyüşü topluluğu için web sitesi. Django + PostgreSQL.
İçerik (etkinlik, SSS, galeri, istatistik) Django admin panelinden yönetilir.

---


## 💻 Yerelde çalıştırma

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # SECRET_KEY doldur (komut README'de)
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```
→ http://127.0.0.1:8000  ·  Admin: http://127.0.0.1:8000/admin/

---

##  Güvenlik

Üretimde (`DEBUG=False`) otomatik aktif olur: HTTPS yönlendirme, HSTS,
güvenli çerezler, clickjacking koruması, `SECRET_KEY` ortam değişkeninden okunur.
`python manage.py check --deploy` üretim modunda **0 uyarı** verir.

##  Yapı
```
config/          Django ayarları, URL'ler
community/       Uygulama: modeller, view'ler, admin, seed komutu
templates/       base.html + sayfa şablonları
static/          CSS, JS
render.yaml      Render blueprint (web + veritabanı)
build.sh         Deploy build script'i
```

## İçerik yönetimi
Admin panelinden yönetilen modeller: **Etkinlikler**, **Aktiviteler**,
**SSS**, **Galeri**, **İstatistikler**. Kod bilmeden içerik güncellenebilir.
