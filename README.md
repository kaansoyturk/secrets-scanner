# 🔑 Secrets Scanner

Kod dosyalarını ve repolarını tarayarak yanlışlıkla commit edilmiş API anahtarları, şifreler ve token'ları tespit eden güvenlik aracı.

## 🔍 Ne Tespit Ediyor?

- AWS Access Key & Secret Key
- GitHub Token
- Google API Key
- Stripe Secret Key
- Private Key (RSA, EC)
- Generic Password & API Key
- Generic Secret & Token
- Database URL (MongoDB, MySQL, PostgreSQL, Redis)

## 🛠️ Teknolojiler

- **Python 3** — Ana dil
- **GitPython** — Git repo desteği
- **Colorama** — Renkli terminal çıktısı
- **Regex** — Kalıp eşleştirme

## 🚀 Kurulum

Repoyu klonla ve bağımlılıkları yükle:

    git clone https://github.com/kaansoyturk/secrets-scanner.git
    cd secrets-scanner
    python3 -m venv venv
    source venv/bin/activate
    pip install gitpython colorama

## ▶️ Kullanım

Bir klasörü taramak için:

    python3 scanner.py /taranacak/klasor

Örnek:

    python3 scanner.py ~/projelerim

## 📸 Örnek Çıktı

    🔍 Taranıyor: /Users/kaansoyturk/projelerim

    [!] Generic Password
        📄 Dosya : emailer.py
        📍 Satır : 6
        🔎 İçerik: GMAIL_APP_PASSWORD = "bjaoaugmzbyfrilv"

    ==================================================
    📊 Taranan dosya : 10
    🚨 Bulunan secret: 1

## ✅ Özellikler

- 9 farklı secret kalıbı tespiti
- Renkli terminal çıktısı
- Klasör bazlı tarama
- Gereksiz dosyaları otomatik atlar

## 👨‍💻 Geliştirici

Kaan Soytürk — [github.com/kaansoyturk](https://github.com/kaansoyturk)