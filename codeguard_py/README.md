# CodeGuard — Python Kod Sağlamlık Analizi (PyQt6)

Cursor/Windsurf benzeri 3-panel masaüstü uygulaması. HTML mockup'ın birebir Python portu.

## Kurulum

```bash
pip install PyQt6
```

## Çalıştırma

```bash
cd codeguard_py
python main.py
```

## Yapı

```
codeguard_py/
├── main.py              Ana pencere + state yönetimi
├── theme.py             Renkler, fontlar, global QSS
├── data.py              Mock proje, dosya ağacı, skorlar, bulgular
├── icons.py             Vector path tabanlı ikonlar (QPainter)
└── widgets/
    ├── titlebar.py      Logo + breadcrumb + komut paleti butonu
    ├── sidebar.py       Proje kartı + dosya ağacı + venv durumu
    ├── gauge.py         Animasyonlu dairesel skor halkası
    ├── highlighter.py   Python syntax highlighter
    ├── center.py        Skorlar / Kod toggle + içerikler
    ├── chat.py          AI chat (sahte cevap üretici)
    ├── command_palette.py  Ctrl+K paleti
    ├── statusbar.py     Alt durum çubuğu
    └── toast.py         Sağ alt bildirimler
```

## Özellikler

- **Dosya seçimi:** Sol panelde dosyaya tıkla → orta panel o dosyanın skorlarını animasyonla yükler.
- **Görünüm toggle:** Üstteki "Skorlar / Kod" butonu ile orta paneli değiştir.
- **Tara butonu:** 2 saniyelik sahte tarama animasyonu + toast bildirimi + gauge'lar yeniden animate.
- **AI Chat:** "imza", "async", "tara", "test" gibi anahtar kelimelere bağlama uygun cevap.
- **Ctrl+K:** Komut paleti — dosya/görünüm/eylem ara.
- **Syntax highlight:** QSyntaxHighlighter ile Python keyword/string/number/comment.
- **Issue gutter:** Kod görünümünde sorunlu satırların arka planı renkli.

## Sıradaki Adımlar (öneriler)

1. **Gerçek analiz:** `bandit` (güvenlik), `ruff`/`pylint` (clean code), `radon` (complexity) entegrasyonu.
2. **Gerçek dosya açma:** `QFileDialog` ile klasör seçtir, `Path.rglob('*.py')` ile gez.
3. **Claude API:** `chat.py` içinde `respond_to` yerine gerçek AI çağrısı.
4. **Tema değiştirme:** Light/Dark toggle.
5. **Kalıcılık:** Son açılan proje, panel boyutları için `QSettings`.
