"""Download Google Fonts collection and extract TTF/OTF files into a folder.

This script downloads the Google Fonts zip archive from the Google Fonts GitHub
mirror (a static URL pointing to the latest master archive), extracts font files
and writes them to the output folder. It deduplicates by filename.
"""
import argparse
import requests
import zipfile
import io
import os
from tqdm import tqdm


GOOGFONTS_ZIP = "https://github.com/google/fonts/archive/refs/heads/main.zip"


def download_and_extract(output_dir: str, subset: str | None = None):
    os.makedirs(output_dir, exist_ok=True)
    print("Downloading Google Fonts archive (this can be large)...")
    r = requests.get(GOOGFONTS_ZIP, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("Content-Length", 0))
    buf = io.BytesIO()
    with tqdm(total=total, unit="B", unit_scale=True) as pbar:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                buf.write(chunk)
                pbar.update(len(chunk))
    buf.seek(0)
    print("Extracting font files...")
    with zipfile.ZipFile(buf) as z:
        members = [m for m in z.namelist() if m.lower().endswith(('.ttf', '.otf'))]
        for m in tqdm(members, desc="Extracting"):
            parts = m.split('/')
            # Put all fonts directly into output_dir, dedupe by basename
            name = os.path.basename(m)
            target = os.path.join(output_dir, name)
            if os.path.exists(target):
                # skip duplicates
                continue
            with z.open(m) as src, open(target, 'wb') as dst:
                dst.write(src.read())
    print("Done. Fonts saved to:", output_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', '-o', default='fonts', help='output dir for fonts')
    args = ap.parse_args()
    download_and_extract(args.output)


if __name__ == '__main__':
    main()
