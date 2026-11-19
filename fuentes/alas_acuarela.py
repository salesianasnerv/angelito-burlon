"""Recorta las alas en acuarela hechas con ChatGPT sobre verde croma
(fuentes/ilustraciones_alas_croma.png) y las guarda con fondo transparente en img/alas.webp.
Uso: python3 fuentes/alas_acuarela.py"""
import pathlib
import numpy as np
from PIL import Image
raiz = pathlib.Path(__file__).resolve().parent.parent
a = np.asarray(Image.open(raiz / 'fuentes' / 'ilustraciones_alas_croma.png').convert('RGB')).astype(float)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
verde = g - np.maximum(r, b)                 # cuánto «verde croma» tiene cada píxel
alfa = np.clip(1 - (verde - 40) / 120, 0, 1)  # >160 = fondo, <40 = ala
# quita el reflejo verde de los bordes
g2 = np.where(verde > 0, np.minimum(g, np.maximum(r, b)), g)
out = np.dstack([r, g2, b, alfa * 255]).astype(np.uint8)
im = Image.fromarray(out, 'RGBA')
im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
im.save(raiz / 'img' / 'alas.webp', quality=88, method=6)
print(im.size)
