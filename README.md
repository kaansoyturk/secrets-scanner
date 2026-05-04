# Secrets Scanner

Kod dosyalarini ve GitHub repolarini tarayarak yanlislikla commit edilmis
API anahtarlari, sifreler ve tokenlari tespit eden guvenlik araci.

## Ne Tespit Ediyor?

- AWS Access Key ve Secret Key
- GitHub, Google, Stripe, Slack, Discord token
- Twitter, Azure, Ethereum anahtarlari
- Private Key (RSA, EC, OpenSSH, PGP)
- Database URL (MongoDB, MySQL, PostgreSQL, Redis)
- Mailgun, Twilio, SendGrid, NPM, PyPI token
- Generic Password, API Key, Secret, Auth Token

## Teknolojiler

- Python 3
- Requests - GitHub API erisimi
- ReportLab - PDF rapor
- Colorama - Renkli terminal ciktisi
- Regex - Kalip eslestirme

## Kurulum

    git clone https://github.com/kaansoyturk/secrets-scanner.git
    cd secrets-scanner
    python3 -m venv venv
    source venv/bin/activate
    pip install requests reportlab colorama

## Kullanim

Klasor tarama:

    python3 scanner.py /taranacak/klasor

GitHub repo tarama:

    python3 scanner.py --github https://github.com/kullanici/repo

GitHub repo (token ile, private repolar icin):

    python3 scanner.py --github https://github.com/kullanici/repo --token GITHUB_TOKEN

## Ozellikler

- 30+ secret kalıbı tespiti
- Klasor bazli tarama
- GitHub repo tarama (public ve private)
- PDF rapor olusturma
- Renkli terminal ciktisi
- Gereksiz dosyalari otomatik atlar

## Gelistirici

Kaan Soyturk - github.com/kaansoyturk