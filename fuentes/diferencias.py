# Genera las escenas del juego «Las diferencias» (img/juegos/dif-*.webp) a partir de las escenas del cuento.
# Cada diferencia: (tipo, x, y, rx, ry, extra) en píxeles de una imagen de 1200 de ancho.
#   hue: gira el color (extra = grados) · clon: tapa con lo que hay desplazado (extra=(dx,dy)) · estrella: pega una estrella (extra=color)
# Imprime el JSON de zonas (en %) para pegarlo en juegos/diferencias.html.
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.join(AQUI, '..')
ESCENAS = {
 'clase': ('escena10a', [('hue', 890, 72, 48, 42, 150), ('hue', 258, 150, 55, 55, 120), ('estrella', 612, 132, 22, 22, '#ffcf3a'),
                         ('hue', 140, 385, 75, 95, 140), ('hue', 696, 66, 36, 36, 280), ('hue', 1036, 200, 32, 55, 200)]),
 'reyes': ('escena07', [('hue', 470, 212, 42, 30, 120), ('hue', 690, 395, 75, 55, 250), ('estrella', 700, 120, 26, 26, '#fff1a8'),
                        ('hue', 916, 275, 36, 30, 160), ('clon', 1062, 632, 75, 32, (-170, 0)), ('hue', 545, 465, 18, 30, 180)]),
 'vuelo': ('escena02', [('hue', 300, 330, 28, 30, 190), ('estrella', 610, 150, 22, 22, '#ffe066'), ('clon', 155, 80, 28, 28, (0, -48)),
                        ('clon', 897, 45, 30, 28, (-70, 25)), ('estrella', 985, 95, 20, 20, '#ff9ec4'), ('hue', 1080, 205, 45, 45, 240)]),
}
def mascara(size, x, y, rx, ry):
    m = Image.new('L', size, 0); ImageDraw.Draw(m).ellipse([x-rx, y-ry, x+rx, y+ry], fill=255)
    return m.filter(ImageFilter.GaussianBlur(4))
def gira(im, grados, x=None, y=None, rx=None, ry=None):
    hsv = np.array(im.convert('HSV')).astype(np.int16)
    if x is not None:  # solo los píxeles del mismo color que el centro del objeto (así no se tiñe la pared de alrededor)
        c = hsv[int(y-ry*.4):int(y+ry*.4)+1, int(x-rx*.4):int(x+rx*.4)+1]
        c = c[c[..., 1] > 60]
        h0 = int(np.median(c[..., 0])) if len(c) else 0
        dh = np.abs(((hsv[..., 0] - h0 + 128) % 256) - 128)
        ok = (dh < 22) & (hsv[..., 1] > 50)
        rot = hsv.copy(); rot[..., 0] = (rot[..., 0] + int(grados / 360 * 255)) % 256; rot[..., 1] = np.minimum(255, rot[..., 1] * 1.15)
        hsv = np.where(ok[..., None], rot, hsv)
        return Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')
    hsv[..., 0] = (hsv[..., 0] + int(grados / 360 * 255)) % 256
    hsv[..., 1] = np.minimum(255, hsv[..., 1] * 1.15)
    return Image.fromarray(hsv.astype(np.uint8), 'HSV').convert('RGB')
def estrella(d, x, y, r, color):
    pts = [(x + (r if i % 2 == 0 else r*.45) * math.sin(i*math.pi/5), y - (r if i % 2 == 0 else r*.45) * math.cos(i*math.pi/5)) for i in range(10)]
    d.polygon(pts, fill=color, outline='#b07a12', width=3)
zonas = {}
for clave, (esc, difs) in ESCENAS.items():
    a = Image.open(os.path.join(RAIZ, 'img/escenas', f'{esc}-1600.webp')).convert('RGB')
    a = a.resize((1200, round(a.height * 1200 / a.width)), Image.LANCZOS); b = a.copy()
    for tipo, x, y, rx, ry, extra in difs:
        m = mascara(a.size, x, y, rx, ry)
        if tipo == 'hue': b = Image.composite(gira(b, extra, x, y, rx, ry), b, m)
        elif tipo == 'clon':
            dx, dy = extra; tapa = b.transform(b.size, Image.AFFINE, (1, 0, dx, 0, 1, dy)); b = Image.composite(tapa, b, m)
        elif tipo == 'estrella': estrella(ImageDraw.Draw(b), x, y, rx, extra)
    a.save(os.path.join(RAIZ, 'img/juegos', f'dif-{clave}-a.webp'), quality=82)
    b.save(os.path.join(RAIZ, 'img/juegos', f'dif-{clave}-b.webp'), quality=82)
    zonas[clave] = {'alto': a.height, 'zonas': [[round(x/12, 2), round(y*100/a.height, 2), round(max(rx, ry, 28)/12, 2)] for _, x, y, rx, ry, _ in difs]}
print(json.dumps(zonas))
