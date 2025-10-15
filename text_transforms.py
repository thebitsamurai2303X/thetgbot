"""Simple Unicode text style transformations to create more unique outputs.

Each transform maps basic ASCII letters/numbers into styled Unicode equivalents
when available. Unmappable characters are left unchanged.
"""
from __future__ import annotations
from typing import Dict
import random

try:
    import pyfiglet
except Exception:
    pyfiglet = None


_styles: Dict[str, Dict[int, str]] = {}


def _build_offset_style(name: str, base_ord: int, digits_base: int | None = None):
    # builds a mapping for A-Z and a-z using offsets where available
    table = {}
    for i in range(26):
        table[ord('A') + i] = chr(base_ord + i)
        table[ord('a') + i] = chr(base_ord + 26 + i) if base_ord else chr(base_ord + i)
    if digits_base:
        for i in range(10):
            table[ord('0') + i] = chr(digits_base + i)
    _styles[name] = table


# We'll create some common styles by explicit maps or offsets where possible.
# Note: Unicode block layout differs; for reliability we build maps manually for
# the styles we support.


def _map_from_pairs(name: str, pairs: Dict[str, str]):
    table = {ord(k): v for k, v in pairs.items()}
    _styles[name] = table


def init_styles():
    # Create multiple Russian style maps
    for style_index in range(8):  # Create 8 different Russian style maps
        russian_stylish_map = {}
        russian_chars = {
            'а': ['𝒂', '𝓪', '𝔞', '𝕒', '𝖆', '𝗮', '𝘢', '𝙖'],
            'б': ['б', 'б̀', 'б̂', 'б̃', 'б̄', 'б̅', 'б̈', 'б̋'],
            'в': ['в', 'в̀', 'в̂', 'в̃', 'в̄', 'в̅', 'в̈', 'в̋'],
        'г': ['г', 'г̀', 'г̂', 'г̃', 'г̄', 'г̅', 'г̈', 'г̋', 'г̌'],
        'д': ['д', 'д̀', 'д̂', 'д̃', 'д̄', 'д̅', 'д̈', 'д̋', 'д̌'],
        'е': ['𝒆', '𝓮', '𝔢', '𝕖', '𝖊', '𝗲', '𝘦', '𝙚', '𝚎'],
        'ё': ['ё', 'ё̀', 'ё̂', 'ё̃', 'ё̄', 'ё̅', 'ё̈', 'ё̋', 'ё̌'],
        'ж': ['ж', 'ж̀', 'ж̂', 'ж̃', 'ж̄', 'ж̅', 'ӝ', 'ж̋', 'ж̌'],
        'з': ['з', 'з̀', 'з̂', 'з̃', 'з̄', 'з̅', 'ӟ', 'з̋', 'з̌'],
        'и': ['и', 'ѝ', 'и̂', 'и̃', 'ӣ', 'и̅', 'ӥ', 'и̋', 'и̌'],
        'й': ['й', 'й̀', 'й̂', 'й̃', 'й̄', 'й̅', 'й̈', 'й̋', 'й̌'],
        'к': ['к', 'к̀', 'к̂', 'к̃', 'к̄', 'к̅', 'к̈', 'к̋', 'к̌'],
        'л': ['л', 'л̀', 'л̂', 'л̃', 'л̄', 'л̅', 'л̈', 'л̋', 'л̌'],
        'м': ['м', 'м̀', 'м̂', 'м̃', 'м̄', 'м̅', 'м̈', 'м̋', 'м̌'],
        'н': ['н', 'н̀', 'н̂', 'н̃', 'н̄', 'н̅', 'н̈', 'н̋', 'н̌'],
        'о': ['𝒐', '𝓸', '𝔬', '𝕠', '𝖔', '𝗼', '𝘰', '𝙤', '𝚘'],
        'п': ['п', 'п̀', 'п̂', 'п̃', 'п̄', 'п̅', 'п̈', 'п̋', 'п̌'],
        'р': ['р', 'р̀', 'р̂', 'р̃', 'р̄', 'р̅', 'р̈', 'р̋', 'р̌'],
        'с': ['с', 'с̀', 'с̂', 'с̃', 'с̄', 'с̅', 'с̈', 'с̋', 'с̌'],
        'т': ['т', 'т̀', 'т̂', 'т̃', 'т̄', 'т̅', 'т̈', 'т̋', 'т̌'],
        'у': ['у', 'у̀', 'у̂', 'у̃', 'ӯ', 'у̅', 'ӱ', 'ӳ', 'у̌'],
        'ф': ['ф', 'ф̀', 'ф̂', 'ф̃', 'ф̄', 'ф̅', 'ф̈', 'ф̋', 'ф̌'],
        'х': ['х', 'х̀', 'х̂', 'х̃', 'х̄', 'х̅', 'х̈', 'х̋', 'х̌'],
        'ц': ['ц', 'ц̀', 'ц̂', 'ц̃', 'ц̄', 'ц̅', 'ц̈', 'ц̋', 'ц̌'],
        'ч': ['ч', 'ч̀', 'ч̂', 'ч̃', 'ч̄', 'ч̅', 'ӵ', 'ч̋', 'ч̌'],
        'ш': ['ш', 'ш̀', 'ш̂', 'ш̃', 'ш̄', 'ш̅', 'ш̈', 'ш̋', 'ш̌'],
        'щ': ['щ', 'щ̀', 'щ̂', 'щ̃', 'щ̄', 'щ̅', 'щ̈', 'щ̋', 'щ̌'],
        'ъ': ['ъ', 'ъ̀', 'ъ̂', 'ъ̃', 'ъ̄', 'ъ̅', 'ъ̈', 'ъ̋', 'ъ̌'],
        'ы': ['ы', 'ы̀', 'ы̂', 'ы̃', 'ы̄', 'ы̅', 'ӹ', 'ы̋', 'ы̌'],
        'ь': ['ь', 'ь̀', 'ь̂', 'ь̃', 'ь̄', 'ь̅', 'ь̈', 'ь̋', 'ь̌'],
        'э': ['э', 'э̀', 'э̂', 'э̃', 'э̄', 'э̅', 'ӭ', 'э̋', 'э̌'],
        'ю': ['ю', 'ю̀', 'ю̂', 'ю̃', 'ю̄', 'ю̅', 'ю̈', 'ю̋', 'ю̌'],
        'я': ['я', 'я̀', 'я̂', 'я̃', 'я̄', 'я̅', 'я̈', 'я̋', 'я̌']
    }
    
        for char, variants in russian_chars.items():
            if style_index < len(variants):
                variant = variants[style_index]
                russian_stylish_map[ord(char)] = variant
                russian_stylish_map[ord(char.upper())] = variant.upper()
            else:
                # If we don't have enough variants, use combining characters
                base = char
                russian_stylish_map[ord(char)] = base + chr(0x0300 + style_index % 8)
                russian_stylish_map[ord(char.upper())] = base.upper() + chr(0x0300 + style_index % 8)
        _styles[f'russian_style_{style_index + 1}'] = russian_stylish_map.copy()

    # Regular styles
    # Fancy script style
    script_map = {}
    for i in range(26):
        script_map[ord('A') + i] = chr(0x1D49C + i)  # Mathematical script capitals
        script_map[ord('a') + i] = chr(0x1D4B6 + i)  # Mathematical script small
    _styles['script'] = script_map

    # Fancy bold script style
    bold_script_map = {}
    for i in range(26):
        bold_script_map[ord('A') + i] = chr(0x1D4D0 + i)  # Mathematical bold script capitals
        bold_script_map[ord('a') + i] = chr(0x1D4EA + i)  # Mathematical bold script small
    _styles['bold_script'] = bold_script_map

    # Sans-serif style
    sans_map = {}
    for i in range(26):
        sans_map[ord('A') + i] = chr(0x1D5A0 + i)  # Mathematical sans-serif capitals
        sans_map[ord('a') + i] = chr(0x1D5BA + i)  # Mathematical sans-serif small
    for i in range(10):
        sans_map[ord('0') + i] = chr(0x1D7E2 + i)  # Mathematical sans-serif digits
    _styles['sans'] = sans_map

    # Bold (Mathematical Bold) - capitals then smalls contiguous
    # A quick static map for letters and digits using their codepoints
    bold_map = {}
    # capitals U+1D400..1D419, lowercase U+1D41A..1D433, digits U+1D7CE..1D7D7
    for i in range(26):
        bold_map[ord('A') + i] = chr(0x1D400 + i)
        bold_map[ord('a') + i] = chr(0x1D41A + i)
    for i in range(10):
        bold_map[ord('0') + i] = chr(0x1D7CE + i)
    _styles['bold'] = bold_map

    # Italic (Mathematical Italic)
    it_map = {}
    for i in range(26):
        it_map[ord('A') + i] = chr(0x1D434 + i)
        it_map[ord('a') + i] = chr(0x1D44E + i)
    _styles['italic'] = it_map

    # Fraktur
    frak_map = {}
    for i in range(26):
        frak_map[ord('A') + i] = chr(0x1D504 + i)
        frak_map[ord('a') + i] = chr(0x1D51E + i)
    _styles['fraktur'] = frak_map

    # Double-struck (blackboard bold)
    dbl_map = {}
    for i in range(26):
        dbl_map[ord('A') + i] = chr(0x1D538 + i)
        dbl_map[ord('a') + i] = chr(0x1D552 + i)
    for i in range(10):
        dbl_map[ord('0') + i] = chr(0x1D7D8 + i)
    _styles['double'] = dbl_map

    # Fullwidth (useful for a novel look)
    fw_map = {}
    for i in range(0x21, 0x7F):
        fw_map[i] = chr(0xFF00 + i)
    _styles['fullwidth'] = fw_map

    # Monospace (Mathematical Monospace)
    mono_map = {}
    for i in range(26):
        mono_map[ord('A') + i] = chr(0x1D670 + i)
        mono_map[ord('a') + i] = chr(0x1D68A + i)
    for i in range(10):
        mono_map[ord('0') + i] = chr(0x1D7F6 + i)
    _styles['monospace'] = mono_map

    # Circled (numbers and letters) - limited support
    circ_map = {}
    for i in range(26):
        circ_map[ord('a') + i] = chr(0x24D0 + i)
        circ_map[ord('A') + i] = chr(0x24B6 + i)
    # map single digits '0'..'9' to circled digits where possible
    # circled 1..9 are U+2460..U+2468, circled 0 is U+24EA
    circ_map[ord('0')] = chr(0x24EA)
    for i in range(1, 10):
        circ_map[ord(str(i))] = chr(0x2460 + i - 1)
    _styles['circled'] = circ_map

    # Squared letters
    squared_map = {}
    for i in range(26):
        squared_map[ord('A') + i] = chr(0x1F130 + i)  # Squared Latin capital letters
    _styles['squared'] = squared_map

    # Regional indicator symbols (flag-like letters)
    regional_map = {}
    for i in range(26):
        regional_map[ord('A') + i] = chr(0x1F1E6 + i)  # Regional indicator symbols
    _styles['regional'] = regional_map

    # Small capitals
    small_caps_map = {}
    for i in range(26):
        small_caps_map[ord('a') + i] = chr(0x1D00 + i)  # Latin letter small capital
    _styles['small_caps'] = small_caps_map

    # Create bubble letters style using enclosed alphanumerics
    bubble_map = {}
    for i in range(26):
        bubble_map[ord('A') + i] = chr(0x24B6 + i)  # Circled latin capital letters
        bubble_map[ord('a') + i] = chr(0x24D0 + i)  # Circled latin small letters
    for i in range(10):
        bubble_map[ord('0') + i] = chr(0x2460 + i) if i > 0 else '⓪'
    _styles['bubble'] = bubble_map

    # Rock dots (heavy circles) style
    rock_map = {}
    for c in 'abcdefghijklmnopqrstuvwxyz':
        rock_map[ord(c)] = c + '̈'  # Combining diaeresis
        rock_map[ord(c.upper())] = c.upper() + '̈'
    _styles['rock'] = rock_map

    # Underline style
    underline_map = {}
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        underline_map[ord(c)] = c + '̲'  # Combining low line
    _styles['underline'] = underline_map

    # Strike through style
    strike_map = {}
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        strike_map[ord(c)] = c + '̶'  # Combining strike through
    _styles['strike'] = strike_map


init_styles()


def available_styles() -> list[str]:
    return sorted(_styles.keys())


def transform(text: str, style: str) -> str:
    if style not in _styles:
        raise KeyError(f'Unknown style: {style}')
    table = _styles[style]
    return text.translate(table)


def _apply_combining(text: str, intensity: int = 1) -> str:
    # add some combining diacritics above/below characters to create messy unique looks
    comb_above = [0x0300, 0x0301, 0x0302, 0x0303, 0x0308, 0x030A]
    comb_below = [0x0323, 0x0324, 0x0325]
    out = []
    for ch in text:
        out.append(ch)
        if ch.strip() and random.random() < 0.25 * intensity:
            out.append(chr(random.choice(comb_above)))
        if ch.strip() and random.random() < 0.15 * intensity:
            out.append(chr(random.choice(comb_below)))
    return ''.join(out)


def _leet(text: str) -> str:
    m = {'a': '4', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '1', 'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7'}
    return ''.join(m.get(c, c) for c in text)


def generate_variants(text: str, max_variants: int = 40) -> list[str]:
    """Return a list of textual 'font' variants for the given text.

    Generates exactly max_variants unique variations using various transformations.
    For Russian text, includes additional Cyrillic-specific transformations.
    """
    # Detect if text contains Russian characters
    has_cyrillic = any(ord('а') <= ord(c) <= ord('я') or ord('А') <= ord(c) <= ord('Я') for c in text)
    
    variants = set()  # Use set to ensure uniqueness
    
    # Get all available styles
    all_styles = available_styles()
    
    # Organize styles based on text content
    if has_cyrillic:
        # Put Russian styles first for Cyrillic text
        russian_styles = [s for s in all_styles if s.startswith('russian_style_')]
        other_styles = [s for s in all_styles if not s.startswith('russian_style_')]
        styles_to_try = russian_styles + other_styles
    else:
        styles_to_try = all_styles
    
    # Apply style transforms
    for style in styles_to_try:
        try:
            variant = transform(text, style)
            if variant != text:  # Only add if the transform actually changed something
                variants.add(variant)
        except Exception:
            continue
            
    # Add combining diacritics variants
    for intensity in range(1, 4):
        variants.add(_apply_combining(text, intensity=intensity))
        
    # Add leet speak variant
    variants.add(_leet(text))

    # Add ASCII art variants if pyfiglet is available
    if pyfiglet:
        # Carefully selected fonts that work well with both Latin and Cyrillic
        fonts = [
            'standard', 'slant', 'small', 'big', 'block', 'bubble',
            'digital', 'mini', 'rounded', 'banner3-D', 'letters',
            'cybermedium', 'cyberlarge', 'doom'
        ]
        for f in fonts:
            try:
                art = pyfiglet.figlet_format(text, font=f)
                if art and art.strip():  # Only add if we got valid output
                    variants.add(art)
            except Exception:
                continue

    # Add original text if not already included
    variants.add(text)
    
    # Convert set to list and ensure we have exactly max_variants
    result = list(variants)
    
    # If we don't have enough variants, add more using combining characters
    while len(result) < max_variants:
        # Create new variants using different combining character patterns
        new_variant = text
        for c in new_variant:
            if random.random() < 0.5:
                # Add random combining diacritical marks
                marks = [chr(x) for x in range(0x0300, 0x0370)]
                new_variant = new_variant.replace(c, c + random.choice(marks))
        result.append(new_variant)
    
    # If we have too many variants, trim to max_variants
    result = result[:max_variants]
    
    return result

