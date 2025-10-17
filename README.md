# ✍️ The Fonts Bot (@fontstgbot)

Made by [@thebitsamurai](https://t.me/thebitsamurai)

---

## 🚨 Important Notice (Development Stage)

> ⚠️ **WARNING: The bot is still under development.**
> 
> Functionality may be incomplete, and you might encounter bugs.
> Please report any issues you find to **@thebitsamurai** on Telegram.
> 
> *A special thanks for your feedback!*

---

## 💡 About The Project

This project is a ready starter for a Telegram bot that renders user text using many fonts downloaded from **Google Fonts**.

The bot is currently available in **8 languages**:
1.  English
2.  Russian
3.  Arabic
4.  Spanish
5.  Azerbaijani
6.  Turkish
7.  French
8.  German

---

## 📂 Project Structure

* `bot.py` - Telegram bot entrypoint
* `renderer.py` - Image rendering utilities (**Pillow**)
* `download_fonts.py` - Script to download and extract Google Fonts
* `requirements.txt` - Python dependencies
* `.env.example` - Example environment variables
* `fonts/` - Directory where downloaded fonts are stored

---

## 🛠️ Setup and Run

### 1. Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
