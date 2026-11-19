"""Genera las imágenes de la web a partir de los originales del proyecto.
Uso: python3 fuentes/preparar_imagenes.py  (desde la carpeta de la web)
Originales: escenas del vídeo (escena00-10.png), PDF del cuento (vista previa) y logo Salesianas.
"""
import subprocess, glob, os, sys
from PIL import Image
PF = "/mnt/project-files"
ESC = f"{PF}/angelito-burlon-video/escenas"
PDF = f"{PF}/Angelito_Burlon_vista_previa-20261117T212321-1719.pdf"
LOGO = sys.argv[1] if len(sys.argv) > 1 else "fuentes/logo_nervion.png"
OUT = "img"

# 1. Escenas limpias (sin texto) -> 1600 y 800 px
for f in sorted(glob.glob(f"{ESC}/escena*.png")):
    n = os.path.basename(f)[:-4]
    im = Image.open(f).convert("RGB")
    for w in (1600, 800):
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f"{OUT}/escenas/{n}-{w}.webp", quality=80)

# 2. Páginas del libro (dobles páginas con texto) para el hojeador
tmp = "/tmp/_libro"; os.makedirs(tmp, exist_ok=True)
subprocess.run(["pdftoppm", "-r", "120", "-png", PDF, f"{tmp}/p"], check=True)
for k, f in enumerate(sorted(glob.glob(f"{tmp}/p-*.png")), 1):
    im = Image.open(f).convert("RGB")
    im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(f"{OUT}/libro/doble{k:02d}.webp", quality=78)

# 3. Recortes del personaje desde el PDF A4 de imprenta (más resolución); fondo blanco -> transparente
A4 = f"{PF}/Angelito_Burlon_A4_para_imprimir-20261117T211354-1a5c.pdf"
recortes = [(2, (573, 787), "angelito-pie"), (15, (806, 772), "angelito-risa"),
            (15, (680, 614), "angelito-vuela"), (16, (443, 488), "angelito-yo")]
for page, size, name in recortes:
    d = f"{tmp}/a4_{page}"; os.makedirs(d, exist_ok=True)
    subprocess.run(["pdfimages", "-j", "-f", str(page), "-l", str(page), A4, f"{d}/i"], check=True)
    for p in glob.glob(f"{d}/i-*"):
        im = Image.open(p)
        if im.size != size:
            continue
        im = im.convert("RGB").convert("RGBA")
        px = im.load(); W, H = im.size
        # solo se borra el blanco conectado con el borde (no el blanco de alas o túnica)
        seen = bytearray(W * H); stack = [(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)]
        while stack:
            x, y = stack.pop()
            if x < 0 or y < 0 or x >= W or y >= H or seen[y * W + x]:
                continue
            seen[y * W + x] = 1
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            if m < 225:
                continue
            px[x, y] = (r, g, b, max(0, min(255, int((255 - m) * 255 / 30))))
            stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        im.save(f"{OUT}/personaje/{name}.webp", quality=88)

# 4. Logo del colegio (Nervión): color y blanco (para fondos oscuros)
lg = Image.open(LOGO).convert("RGBA")
lg = lg.crop(lg.getchannel("A").getbbox())
lg = lg.resize((1200, round(lg.height * 1200 / lg.width)), Image.LANCZOS)
lg.save(f"{OUT}/logos/nervion-color.png", optimize=True)
w = Image.new("RGBA", lg.size, (255, 255, 255, 0)); w.putalpha(lg.getchannel("A"))
w.save(f"{OUT}/logos/nervion-blanco.png", optimize=True)
print("Listo")
