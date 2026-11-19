"""Genera los adornos de alas que separan las páginas de papel de la web.
  img/alas.svg  -> par de alas doradas con estrella en el centro (no se deforma)
  img/borde.svg -> filo del papel: curva suave que sube hacia el centro
Uso: python3 fuentes/alas_separador.py"""
import math, pathlib
RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAPEL, ORO, ORO_CLARO = '#fff6e6', '#d99a22', '#f8dc93'

def pluma(x, y, ang, largo, ancho):
    """Pluma en forma de hoja: base en (x,y), apunta en el ángulo dado (grados)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)          # a lo largo
    px, py = -uy, ux                           # perpendicular
    tx, ty = x + ux * largo, y + uy * largo
    c1 = (x + ux * largo * .35 + px * ancho, y + uy * largo * .35 + py * ancho)
    c2 = (x + ux * largo * .85 + px * ancho * .9, y + uy * largo * .85 + py * ancho * .9)
    c3 = (x + ux * largo * .8 - px * ancho * .55, y + uy * largo * .8 - py * ancho * .55)
    c4 = (x + ux * largo * .3 - px * ancho * .6, y + uy * largo * .3 - py * ancho * .6)
    f = lambda p: f'{p[0]:.1f},{p[1]:.1f}'
    cuerpo = f'M{f((x, y))} C{f(c1)} {f(c2)} {f((tx, ty))} C{f(c3)} {f(c4)} {f((x, y))}Z'
    raquis = f'M{f((x, y))} Q{f((x + ux * largo * .5 + px * ancho * .15, y + uy * largo * .5 + py * ancho * .15))} {f((x + ux * largo * .82, y + uy * largo * .82))}'
    return cuerpo, raquis

def ala():
    """Ala izquierda; el hombro está en (0,0) y se abre hacia la izquierda y arriba."""
    capas = []
    # remeras (largas), de abajo hacia arriba
    for i in range(8):
        ang = 180 + i * 6.8
        largo = 128 - abs(i - 5) * 8
        capas.append(pluma(-8 - i * 2, 6 - i * 1.5, ang, largo, 13))
    # coberteras (cortas) por encima
    for i in range(6):
        ang = 190 + i * 8
        capas.append(pluma(-4, -2, ang, 66 - i * 3, 12))
    # hombro redondeado
    for i in range(3):
        ang = 205 + i * 15
        capas.append(pluma(0, -4, ang, 30, 10))
    return capas

def svg_alas():
    W, H = 340, 140
    cx, cy = W / 2, 104
    g = []
    for lado, tr in ((-1, f'translate({cx - 16} {cy})'), (1, f'translate({cx + 16} {cy}) scale(-1 1)')):
        trozos = ''.join(f'<path d="{c}"/><path class="r" d="{r}"/>' for c, r in ala())
        g.append(f'<g transform="{tr}">{trozos}</g>')
    estrella = ('<path d="M170 84l7.6 17.3 18.8 1.6-14.3 12.4 4.3 18.4L170 124l-16.2 9.7 4.3-18.4-14.3-12.4 18.8-1.6z" '
                f'fill="{ORO_CLARO}" stroke="{ORO}" stroke-width="3" stroke-linejoin="round"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
            f'<style>path{{fill:{PAPEL};stroke:{ORO};stroke-width:2.2;stroke-linejoin:round}}'
            f'path.r{{fill:none;stroke:{ORO_CLARO};stroke-width:1.6;stroke-linecap:round}}</style>'
            + ''.join(g) + estrella + '</svg>')

def svg_borde():
    W, H = 1440, 60
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">'
            f'<path d="M0 {H} L0 44 C360 44 520 4 720 4 C920 4 1080 44 1440 44 L1440 {H}Z" fill="{PAPEL}"/>'
            f'<path d="M0 44 C360 44 520 4 720 4 C920 4 1080 44 1440 44" fill="none" stroke="{ORO_CLARO}" stroke-width="3" vector-effect="non-scaling-stroke"/></svg>')

(RAIZ / 'img' / 'alas.svg').write_text(svg_alas())
(RAIZ / 'img' / 'borde.svg').write_text(svg_borde())
print('img/alas.svg e img/borde.svg listos')
