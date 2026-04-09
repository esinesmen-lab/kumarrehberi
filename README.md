# 🎰 KumarRehberi - Otomatik Makale Sistemi

Her **Pazartesi**, **Çarşamba** ve **Cuma** saat 12:00'de otomatik makale üretir!

---

## ⚡ Kurulum (10 dakika)

### 1. Bu Repo'yu GitHub'a Yükle
Tüm bu dosyaları GitHub reposuna yükle.

### 2. Netlify Bağlantısı
1. [netlify.com](https://netlify.com) → "New site from Git"
2. Bu GitHub reposunu seç
3. Deploy settings: Build command boş, Publish directory: `.`
4. **Deploy!**

### 3. Claude API Key Ekle (GİZLİ)
1. GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. **"New repository secret"** tıkla
3. Name: `ANTHROPIC_API_KEY`
4. Value: API key'ini yapıştır
5. **Add secret** tıkla

### 4. Hazır! 🎉
- Her Pazartesi/Çarşamba/Cuma sabahı otomatik makale üretilir
- Makale `makaleler/` klasörüne kaydedilir
- `sitemap.xml` otomatik güncellenir
- Netlify otomatik deploy eder

---

## 📅 Makale Takvimi (12 Konulu Döngü)

| Hafta | Pazartesi | Çarşamba | Cuma |
|-------|-----------|----------|------|
| 1 | Sweet Bonanza Stratejisi | En Yüksek RTP Slotlar | Hoşgeldin Bonusu Rehberi |
| 2 | Gates of Olympus | Canlı Casino vs Slot | Value Bet Rehberi |
| 3 | Big Bass Bonanza | Para Çekme Yöntemleri | Rulet Stratejileri |
| 4 | Dog House Megaways | Güvenilir Casino Seçimi | Freespin Bonusları |

---

## 🔧 Manuel Çalıştırma
GitHub → **Actions** → **Otomatik Makale Üret** → **Run workflow**

---

## 📁 Dosya Yapısı
```
/
├── index.html          ← Ana sayfa
├── go.html             ← Yönlendirme sayfası
├── sitemap.xml         ← Otomatik güncellenir
├── robots.txt
├── makaleler/          ← Otomatik oluşturulur
│   ├── sweet-bonanza-stratejisi.html
│   └── ...
├── scripts/
│   └── makale_uret.py  ← Makale üretici
└── .github/
    └── workflows/
        └── makale-uret.yml  ← Zamanlama
```
