#!/usr/bin/env python3
"""Copia los carteles A3 a la web y hace sus miniaturas.
Uso: python3 fuentes/carteles_web.py <carpeta con los PDF «… - dos caras DIN A3.pdf»>
Los PDF se generan con angelito-carteles/fuentes/build.py (copia en OneDrive Carteles/fuentes).
"""
import sys, subprocess, unicodedata, re, shutil, tempfile
from pathlib import Path
from PIL import Image
RAIZ = Path(__file__).resolve().parent.parent
def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')
for pdf in sorted(Path(sys.argv[1]).glob('* - dos caras DIN A3.pdf')):
    titulo = pdf.name.replace(' - dos caras DIN A3.pdf', '')
    s = slug(titulo)
    shutil.copy(pdf, RAIZ / 'pdf/carteles' / f'Cartel_A3_{s}.pdf')
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['pdftoppm', '-r', '50', '-png', '-f', '1', '-l', '1', str(pdf), f'{d}/p'], check=True)
        im = Image.open(next(Path(d).glob('p*.png'))).convert('RGB')
        im.thumbnail((420, 600), Image.LANCZOS)
        im.save(RAIZ / 'img/carteles' / f'{s}.webp', quality=82)
    print(s, '|', titulo)
