# The Fonts @fontstgbot (Made by @thebitsamurai)


> [! WARNING]
> **The bot is still under development.** Functionality may be incomplete, and you might encounter bugs.
> 
> Please report any issues you find to **@thebitsamurai** on Telegram. Thank You!

This project is a ready starter for a Telegram bot that renders user text using many fonts downloaded from Google Fonts. The bot is available on 8 languages: 1. Arabian, 2. Russian 3. Arabic. 4. Spanish 5. Azerbaijani 6. Turkish 7. French 8. German 

Files:
- `bot.py` - Telegram bot entrypoint
- `renderer.py` - Image rendering utilities (Pillow)
- `download_fonts.py` - Script to download and extract Google Fonts
- `requirements.txt` - Python deps
- `.env.example` - Example environment variables
- `fonts/` - Directory where downloaded fonts are stored

Setup

1. Create virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `TELEGRAM_TOKEN`.

3. Run the font downloader to populate `fonts/`:

```bash
python download_fonts.py --output fonts --subset "latin,latin-ext" --min_quality ttf
```

4. Run the bot:

```bash
python bot.py
```

Notes
- Fonts must be used according to their licenses. Google Fonts are generally permissive for this use-case.
- The downloader can take time and disk space; consider selecting subsets like `latin` to reduce size.

```bash
Other projects: t.me/ytdlpload_bot
```
