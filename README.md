# Kaçkar Peak

Koşu, yoga ve doğa yürüyüşü topluluğu için web sitesi. Django + PostgreSQL.
İçerik (etkinlik, SSS, galeri, istatistik) Django admin panelinden yönetilir.

---

### 1. GitHub'a yükle
```bash
git init
git add .
git commit -m "İlk sürüm"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/kackar-peak.git
git push -u origin main
```

### 2. Render'da yayınla
1. [render.com](https://render.com) → GitHub ile giriş yap (ücretsiz).
2. **New → Blueprint** → bu repoyu seç.
3. Render `render.yaml`'ı okur; web servisi **ve** PostgreSQL veritabanını otomatik kurar.
4. **Apply** de. İlk deploy ~3-5 dakika sürer.
5. Bittiğinde üstteki `.onrender.com` linki senin canlı siten — müşterinle paylaşabilirsin.

### 3. Yönetici hesabı ve örnek içerik
Render panelinde servis → **Shell** sekmesi:
```bash
python manage.py createsuperuser   # admin girişi için
python manage.py seed_demo         # örnek etkinlik/SSS ekler (opsiyonel)
```
Ardından `siten.onrender.com/admin/` adresinden içerik girebilirsin.

> Not: Render ücretsiz plan, site 15 dk kullanılmazsa uykuya geçer; ilk açılış
> birkaç saniye gecikir. Demo/müşteri gösterimi için sorun değil.

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

## 🔒 Güvenlik

Üretimde (`DEBUG=False`) otomatik aktif olur: HTTPS yönlendirme, HSTS,
güvenli çerezler, clickjacking koruması, `SECRET_KEY` ortam değişkeninden okunur.
`python manage.py check --deploy` üretim modunda **0 uyarı** verir.

## 📁 Yapı
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
