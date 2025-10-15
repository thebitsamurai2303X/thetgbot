from __future__ import annotations
from io import BytesIO
import os
import random
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter


FONTS_DIR = os.environ.get('FONTS_DIR', 'fonts')


def list_fonts() -> list[str]:
    if not os.path.isdir(FONTS_DIR):
        return []
    return [os.path.join(FONTS_DIR, f) for f in os.listdir(FONTS_DIR) if f.lower().endswith(('.ttf', '.otf'))]


def pick_font(size: int = 72, text: str = None) -> str:
    fonts = list_fonts()
    if not fonts:
        # return None to indicate no external fonts available
        return None
        
    # Check if text contains Cyrillic characters
    has_cyrillic = any(ord('а') <= ord(c) <= ord('я') or ord('А') <= ord(c) <= ord('Я') for c in text) if text else False
    
    # Filter fonts that support needed characters
    suitable_fonts = []
    for font_path in fonts:
        try:
            font = ImageFont.truetype(font_path, size=size)
            # Test if font supports the first character of the text (as a basic check)
            if text and text[0]:
                if font.getmask(text[0]):
                    suitable_fonts.append(font_path)
            else:
                suitable_fonts.append(font_path)
        except Exception:
            continue
    
    if suitable_fonts:
        return random.choice(suitable_fonts)
    return random.choice(fonts)  # Fallback to any font if no suitable ones found


def measure_text(text: str, font: ImageFont.FreeTypeFont) -> Tuple[int,int]:
    dummy = Image.new('RGBA', (1,1))
    draw = ImageDraw.Draw(dummy)
    return draw.textsize(text, font=font)


def render_text_image(text: str, font_path: str, size: int = 72, padding: int = 24) -> BytesIO:
    if font_path:
        try:
            font = ImageFont.truetype(font_path, size=size)
        except Exception:
            # fallback to default font if truetype fails
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()
    w, h = measure_text(text, font)
    img_w = w + padding * 2
    img_h = h + padding * 2
    img = Image.new('RGBA', (img_w, img_h), (255,255,255,0))
    draw = ImageDraw.Draw(img)

    # Draw shadow
    shadow_offset = max(2, size // 24)
    shadow_color = (0,0,0,160)
    x = padding
    y = padding
    draw.text((x+shadow_offset, y+shadow_offset), text, font=font, fill=shadow_color)

    # Draw main text
    draw.text((x, y), text, font=font, fill=(20,20,20,255))

    # Random subtle filter
    if random.random() < 0.25:
        img = img.filter(ImageFilter.SMOOTH)

    bio = BytesIO()
    img.convert('RGBA').save(bio, 'PNG')
    bio.seek(0)
    return bio
