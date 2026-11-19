"""Convierte las ilustraciones nuevas (ChatGPT, guardadas en PNG en
/mnt/project-files/angelito-burlon-web-fuentes/ilustraciones/ o fuentes/ilustraciones/)
en webp para la web: img/nuevas/<nombre>-1600.webp y -800.webp.
Uso: python3 fuentes/ilustraciones_nuevas.py [carpeta_png]"""
import sys, pathlib
from PIL import Image
raiz = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else raiz / 'fuentes' / 'ilustraciones'
for f in sorted(src.glob('*.png')):
    im = Image.open(f).convert('RGB')
    for w in (1600, 800):
        if im.width < w and w == 1600: w = im.width
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(raiz / 'img' / 'nuevas' / f'{f.stem}-{w if w in (800,) else 1600}.webp', quality=82)
    print(f.stem)
