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


def generate_variants(text: str, max_variants: int = 12) -> list[str]:
    """Return a list of textual 'font' variants for the given text.

    Variants include: unicode style transforms (from _styles), ascii art (pyfiglet),
    leet, and combining diacritics mixes.
    """
    variants = []
    # Unicode styles
    for style in available_styles():
        try:
            variants.append(transform(text, style))
        except Exception:
            continue
        if len(variants) >= max_variants:
            return variants

    # leet
    variants.append(_leet(text))
    if len(variants) >= max_variants:
        return variants

    # combining diacritics variants
    for i in range(1, 3):
        variants.append(_apply_combining(text, intensity=i))
        if len(variants) >= max_variants:
            return variants

    # pyfiglet ascii art styles (if available)
    if pyfiglet:
        # try a larger set of figlet fonts for more uniqueness
        fonts = [
            'standard', 'slant', 'big', 'small', 'banner3-D', 'cybersmall', 'bubble', 'digital',
            'isometric1', 'letters', 'mini', 'ogre', 'smslant', 'larry3d', 'starwars', 'smscript',
            'doh', 'epic', 'block', 'rounded'
        ]
        for f in fonts:
            try:
                variants.append(pyfiglet.figlet_format(text, font=f))
            except Exception:
                continue
            if len(variants) >= max_variants:
                return variants

    # fallback: original
    if text not in variants:
        variants.append(text)
    return variants

