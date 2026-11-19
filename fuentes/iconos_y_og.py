"""Genera favicon, iconos de la PWA e imagen para compartir (WhatsApp/redes).
Uso, desde la carpeta de la web: python3 fuentes/iconos_y_og.py
Necesita Pillow y las fuentes Mountains of Christmas y Kurale (se descargan de Google Fonts si faltan)."""
import os, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
NOCHE = (12, 21, 66); ORO = (245, 196, 81); ORO_CLARO = (255, 231, 163)
FD = "fuentes/tipos"; os.makedirs(FD, exist_ok=True)
TIPOS = {"MountainsofChristmas-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/mountainsofchristmas/MountainsofChristmas-Bold.ttf",
         "Kurale-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/kurale/Kurale-Regular.ttf"}
for n, u in TIPOS.items():
    if not os.path.exists(f"{FD}/{n}"):
        urllib.request.urlretrieve(u, f"{FD}/{n}")

# --- Icono: carita del angelito en un círculo de noche con borde dorado ---
ang = Image.open("img/personaje/angelito-pie.webp").convert("RGBA")
def icono(size, maskable=False):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if maskable:
        d.rectangle([0, 0, size, size], fill=NOCHE + (255,)); pad = int(size * .14)
    else:
        m = max(1, size // 32); d.ellipse([0, 0, size - 1, size - 1], fill=ORO + (255,)); d.ellipse([m, m, size - 1 - m, size - 1 - m], fill=NOCHE + (255,)); pad = int(size * .06)
    # cabeza y alas del angelito, grande y centrada; lo que sobra lo recorta el círculo
    w, h = ang.size; cab = ang.crop((0, 0, w, int(h * .80)))
    escala = (size - 2 * pad) * 1.12 / w; cab = cab.resize((max(1, round(w * escala)), max(1, round(cab.height * escala))), Image.LANCZOS)
    lienzo = Image.new("RGBA", (size, size), (0, 0, 0, 0)); lienzo.alpha_composite(cab, ((size - cab.width) // 2, pad + int(size * .02)))
    if maskable: im.alpha_composite(lienzo)
    else:
        inner = Image.new("L", (size, size), 0); m = max(1, size // 32); ImageDraw.Draw(inner).ellipse([m, m, size - 1 - m, size - 1 - m], fill=255)
        lienzo.putalpha(Image.composite(lienzo.getchannel("A"), Image.new("L", (size, size), 0), inner)); im.alpha_composite(lienzo)
    if not maskable:  # recorta a círculo
        mk = Image.new("L", (size, size), 0); ImageDraw.Draw(mk).ellipse([0, 0, size - 1, size - 1], fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (size, size), 0), mk))
    return im
for s in (16, 32, 48, 192, 512):
    icono(s).save(f"icons/icon-{s}.png", optimize=True)
icono(512, True).save("icons/maskable-512.png", optimize=True)
icono(180, True).convert("RGB").save("icons/apple-touch-icon.png", optimize=True)
icono(48).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# --- Imagen para compartir 1200x630 ---
W, H = 1200, 630
bg = Image.open("img/escenas/escena00-1600.webp").convert("RGB")
bg = bg.resize((W, round(bg.height * W / bg.width)), Image.LANCZOS).crop((0, 0, W, H)) if bg.height * W / bg.width >= H else bg.resize((round(bg.width * H / bg.height), H)).crop((0, 0, W, H))
og = bg.convert("RGBA")
grad = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(grad)
for x in range(W):
    a = int(max(0, min(1, (x - W * .3) / (W * .45))) * 190); gd.line([(x, 0), (x, H)], fill=NOCHE + (a,))
og.alpha_composite(grad)
t1 = ImageFont.truetype(f"{FD}/MountainsofChristmas-Bold.ttf", 104)
t2 = ImageFont.truetype(f"{FD}/MountainsofChristmas-Bold.ttf", 52)
t3 = ImageFont.truetype(f"{FD}/Kurale-Regular.ttf", 30)
capa = Image.new("RGBA", (W, H)); cd = ImageDraw.Draw(capa)
x0 = 560
cd.text((x0, 150), "Angelito", font=t1, fill=ORO + (255,)); cd.text((x0, 255), "Burlón", font=t1, fill=ORO + (255,))
cd.text((x0 + 4, 375), "y la estrella de Navidad", font=t2, fill=ORO_CLARO + (255,))
cd.text((x0 + 6, 452), "Adviento 2026 · Cuento, vídeo y proyectos", font=t3, fill=(238, 241, 255, 255))
brillo = capa.filter(ImageFilter.GaussianBlur(8)); og.alpha_composite(Image.eval(brillo, lambda v: v // 2)); og.alpha_composite(capa)
logo = Image.open("img/logos/nervion-blanco.png").convert("RGBA"); logo.thumbnail((300, 100), Image.LANCZOS)
og.alpha_composite(logo, (x0 + 4, 515))
og.convert("RGB").save("img/og.jpg", quality=86)
print("Listo")
