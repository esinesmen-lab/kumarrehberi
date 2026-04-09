#!/usr/bin/env python3
"""
KumarRehberi - Otomatik Makale Üretici
Her çalıştığında 1 makale üretir ve index.html'e ekler
"""

import anthropic
import os
import json
import re
from datetime import datetime, date
import random

# ─── MAKALE KONULARI (12 haftalık döngü) ────────────────────────────────────
KONULAR = [
    # Hafta 1
    {"baslik": "Sweet Bonanza Stratejisi: 2025'te Kazanma Taktikleri", "anahtar": "Sweet Bonanza strateji, slot kazanma, pragmatic play"},
    {"baslik": "En Yüksek RTP'li Slot Oyunları 2025", "anahtar": "yüksek RTP slot, en iyi slot, casino oyunları"},
    {"baslik": "Hoşgeldin Bonusu Nasıl Kullanılır? Tam Rehber", "anahtar": "hoşgeldin bonusu, casino bonus, çevrim şartı"},
    # Hafta 2
    {"baslik": "Gates of Olympus: Zeus Slot Rehberi ve İpuçları", "anahtar": "Gates of Olympus, Zeus slot, Pragmatic Play"},
    {"baslik": "Canlı Casino vs Slot: Hangisi Daha Kazançlı?", "anahtar": "canlı casino, slot farkı, casino karşılaştırma"},
    {"baslik": "Spor Bahislerinde Value Bet Nasıl Bulunur?", "anahtar": "value bet, spor bahis stratejisi, bahis taktikleri"},
    # Hafta 3
    {"baslik": "Big Bass Bonanza Oyun Rehberi 2025", "anahtar": "Big Bass Bonanza, Pragmatic Play, slot rehberi"},
    {"baslik": "Casino Para Çekme Yöntemleri: En Hızlı Seçenekler", "anahtar": "casino para çekme, papara casino, kripto para casino"},
    {"baslik": "Rulet Stratejileri: Martingale ve Fibonacci Sistemi", "anahtar": "rulet stratejisi, martingale, canlı rulet"},
    # Hafta 4
    {"baslik": "Dog House Megaways Oynanış Rehberi", "anahtar": "Dog House slot, Megaways, Pragmatic Play"},
    {"baslik": "Güvenilir Casino Nasıl Seçilir? 10 Kritik Kriter", "anahtar": "güvenilir casino, lisanslı casino, casino seçimi"},
    {"baslik": "Freespin Bonusları: En İyi Casino Teklifleri 2025", "anahtar": "freespin, bedava döndürme, casino freespin"},
]

# ─── BUGÜN HANGİ KONU? ───────────────────────────────────────────────────────
def konu_sec():
    """Hafta numarasına ve gün indexine göre konu seç"""
    bugun = date.today()
    hafta_no = bugun.isocalendar()[1]
    gun = bugun.weekday()  # 0=Pazartesi, 2=Çarşamba, 4=Cuma

    # Gun indexi belirle (0,1,2)
    gun_map = {0: 0, 2: 1, 4: 2}
    gun_index = gun_map.get(gun, random.randint(0, 2))

    # 4 haftalık döngü
    donem = ((hafta_no - 1) % 4)
    konu_index = (donem * 3) + gun_index

    return KONULAR[konu_index % len(KONULAR)]


# ─── CLAUDE API İLE MAKALE YAZDIR ─────────────────────────────────────────────
def makale_yaz(konu):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""Sen KumarRehberi.com için içerik yazıyorsun. 
Konu: {konu['baslik']}
Anahtar kelimeler: {konu['anahtar']}

500-600 kelimelik, SEO optimize Türkçe makale yaz.

KURALLAR:
- H2 ve H3 başlıklar kullan
- Doğal, akıcı Türkçe
- Her paragraf 3-5 cümle
- Anahtar kelimeleri doğal yerleştir
- Affiliate link için şu placeholder kullan: [CASINO_LINK]
- Makaleyi HTML formatında döndür (<h2>, <h3>, <p> tagları ile)
- <article> veya başka wrapper tag kullanma, sadece içerik tagları
- Sonuna şu CTA ekle: <div class="makale-cta"><a href="[CASINO_LINK]" rel="nofollow" target="_blank" class="btn-primary">🎁 En İyi Bonusu Al</a></div>

SADECE HTML içeriği döndür, başka açıklama ekleme."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# ─── HTML MAKALE SAYFASI OLUŞTUR ──────────────────────────────────────────────
def makale_html_olustur(konu, icerik, slug):
    tarih = datetime.now().strftime("%Y-%m-%d")
    tarih_goster = datetime.now().strftime("%d %B %Y")

    # Affiliate linki değiştir
    icerik = icerik.replace("[CASINO_LINK]", "https://www.hellocasino365.com/go")

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{konu['baslik']} | KumarRehberi</title>
<meta name="description" content="{konu['baslik']} - KumarRehberi.com'da detaylı rehber ve taktikler.">
<meta name="keywords" content="{konu['anahtar']}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://kumarrehberi.com/makaleler/{slug}.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
:root {{
  --gold: #F5A623; --gold2: #FFD166; --dark: #0A0A0F;
  --dark2: #12121A; --dark3: #1A1A26; --card: #1E1E2E;
  --border: rgba(255,255,255,0.08); --text: #E8E8F0;
  --muted: #8888A8; --green: #06D6A0;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Inter',sans-serif; background:var(--dark); color:var(--text); line-height:1.8; }}
nav {{ position:sticky; top:0; z-index:100; background:rgba(10,10,15,0.95); backdrop-filter:blur(10px); border-bottom:1px solid var(--border); padding:0 40px; }}
.nav-inner {{ max-width:1200px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; height:64px; }}
.logo {{ font-family:'Playfair Display',serif; font-size:22px; color:var(--gold); text-decoration:none; font-weight:700; }}
.makale-wrap {{ max-width:800px; margin:60px auto; padding:0 24px 80px; }}
.makale-baslik {{ font-family:'Playfair Display',serif; font-size:36px; font-weight:800; line-height:1.3; margin-bottom:16px; }}
.makale-meta {{ color:var(--muted); font-size:14px; margin-bottom:40px; padding-bottom:20px; border-bottom:1px solid var(--border); }}
.makale-wrap h2 {{ font-size:24px; font-weight:700; color:var(--gold); margin:36px 0 14px; }}
.makale-wrap h3 {{ font-size:18px; font-weight:600; margin:24px 0 10px; }}
.makale-wrap p {{ margin-bottom:18px; color:var(--text); }}
.makale-cta {{ text-align:center; margin:40px 0; padding:32px; background:var(--card); border-radius:16px; border:1px solid rgba(245,166,35,0.2); }}
.btn-primary {{ background:var(--gold); color:var(--dark); padding:14px 32px; border-radius:10px; font-weight:700; font-size:16px; text-decoration:none; display:inline-block; }}
.btn-primary:hover {{ background:var(--gold2); }}
footer {{ text-align:center; padding:40px; color:var(--muted); font-size:14px; border-top:1px solid var(--border); }}
</style>
</head>
<body>
<nav>
  <div class="nav-inner">
    <a href="/" class="logo">Kumar<span>Rehberi</span></a>
    <a href="https://www.hellocasino365.com/go" rel="nofollow" target="_blank" style="background:var(--gold);color:var(--dark);padding:8px 20px;border-radius:8px;font-weight:700;font-size:14px;text-decoration:none;">🎁 Bonus Al</a>
  </div>
</nav>

<div class="makale-wrap">
  <h1 class="makale-baslik">{konu['baslik']}</h1>
  <div class="makale-meta">📅 {tarih_goster} &nbsp;|&nbsp; ✍️ KumarRehberi Editörü &nbsp;|&nbsp; ⏱️ 3 dk okuma</div>
  {icerik}
</div>

<footer>
  <p>© 2025 KumarRehberi.com — 18+ Sorumlu Oynayın</p>
  <p style="margin-top:8px;font-size:12px;">Kumar bağımlılığı için yardım: <a href="https://www.begamblingaware.org" style="color:var(--gold);">BeGambleAware.org</a></p>
</footer>
</body>
</html>"""


# ─── INDEX.HTML'E MAKALE KARTI EKLE ──────────────────────────────────────────
def index_guncelle(konu, slug, tarih_goster):
    index_path = "index.html"
    if not os.path.exists(index_path):
        print("index.html bulunamadı, atlandı")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Makale kartı
    kart = f"""
    <!-- MAKALE: {slug} -->
    <div class="makale-kart" style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:16px;">
      <div style="font-size:12px;color:var(--muted);margin-bottom:8px;">📅 {tarih_goster}</div>
      <h3 style="font-size:18px;font-weight:700;margin-bottom:10px;">{konu['baslik']}</h3>
      <a href="makaleler/{slug}.html" style="color:var(--gold);font-weight:600;font-size:14px;text-decoration:none;">Devamını Oku →</a>
    </div>"""

    # index.html'de "<!-- MAKALELER -->" placeholder'ı varsa oraya ekle
    if "<!-- MAKALELER -->" in html:
        html = html.replace("<!-- MAKALELER -->", f"<!-- MAKALELER -->\n{kart}")
    else:
        # Yoksa </main> veya </body>'den önce ekle
        html = html.replace("</body>", f"\n<!-- MAKALELER -->{kart}\n</body>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ index.html güncellendi")


# ─── SITEMAP GÜNCELLE ─────────────────────────────────────────────────────────
def sitemap_guncelle(slug):
    tarih = datetime.now().strftime("%Y-%m-%d")
    url = f"  <url>\n    <loc>https://kumarrehberi.com/makaleler/{slug}.html</loc>\n    <lastmod>{tarih}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"

    sitemap_path = "sitemap.xml"
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            sm = f.read()
        sm = sm.replace("</urlset>", f"{url}\n</urlset>")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(sm)
        print("✅ sitemap.xml güncellendi")


# ─── ANA ÇALIŞMA ──────────────────────────────────────────────────────────────
def main():
    print(f"🚀 Makale üretimi başlıyor - {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    konu = konu_sec()
    print(f"📝 Konu: {konu['baslik']}")

    # Slug oluştur
    slug = konu['baslik'].lower()
    slug = re.sub(r'[ğ]', 'g', slug)
    slug = re.sub(r'[ü]', 'u', slug)
    slug = re.sub(r'[ş]', 's', slug)
    slug = re.sub(r'[ı]', 'i', slug)
    slug = re.sub(r'[ö]', 'o', slug)
    slug = re.sub(r'[ç]', 'c', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = slug[:60]

    # Makale oluştur
    print("✍️  Claude API'ye bağlanıyor...")
    icerik = makale_yaz(konu)
    print(f"✅ Makale yazıldı ({len(icerik.split())} kelime)")

    # HTML sayfası kaydet
    os.makedirs("makaleler", exist_ok=True)
    html = makale_html_olustur(konu, icerik, slug)
    dosya = f"makaleler/{slug}.html"
    with open(dosya, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Kaydedildi: {dosya}")

    tarih_goster = datetime.now().strftime("%d %B %Y")
    index_guncelle(konu, slug, tarih_goster)
    sitemap_guncelle(slug)

    print(f"\n🎉 Tamamlandı! Makale: {dosya}")


if __name__ == "__main__":
    main()
