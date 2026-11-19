"""Recorta las alas en acuarela (fuentes/ilustraciones_alas.png, fondo blanco, hechas con ChatGPT)
y las guarda con fondo transparente en img/alas.webp y img/alas.png.
Uso: python3 fuentes/alas_acuarela.py"""
import pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageChops
raiz = pathlib.Path(__file__).resolve().parent.parent
im = Image.open(raiz / 'fuentes' / 'ilustraciones_alas.png').convert('RGB')
W, H = im.size
# máscara: todo lo que se conecta con el borde y es casi blanco = fondo
marca = im.copy()
for p in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1), (W // 2, 2), (W // 2, H - 3), (2, H // 2), (W - 3, H // 2)]:
    ImageDraw.floodfill(marca, p, (255, 0, 255), thresh=10)
fondo = Image.eval(ImageChops.difference(marca, Image.new('RGB', (W, H), (255, 0, 255))).convert('L'), lambda v: 255 if v < 8 else 0)
fg = Image.eval(fondo, lambda v: 255 - v)
# cierra huecos del borde de las plumas (zonas blancas pegadas al fondo)
fg = fg.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.MinFilter(21))
alfa = fg.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
im.putalpha(alfa)
bbox = alfa.getbbox(); im = im.crop(bbox)
im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
im.save(raiz / 'img' / 'alas.webp', quality=88); im.save(raiz / 'img' / 'alas.png', optimize=True)
print(im.size)
