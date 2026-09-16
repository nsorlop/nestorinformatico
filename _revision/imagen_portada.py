#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera img/portada.png (la imagen que sale al compartir el enlace) e
icono-180.png. Usa las fuentes de Windows solo para dibujar la imagen.

    python _revision/imagen_portada.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

NOMBRE = 'Néstor el Informático'
LEMA = 'Te lo arreglo y te lo explico'
TELEFONO = '644 21 91 18'


def fuente(nombres, tam):
    for n in nombres:
        p = os.path.join(r'C:\Windows\Fonts', n)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, tam)
            except Exception:
                pass
    return ImageFont.load_default()


NEGRA = ['segoeuib.ttf', 'arialbd.ttf']
NORMAL = ['segoeui.ttf', 'arial.ttf']

FONDO = (16, 31, 26)
CREMA = (236, 235, 226)
VERD = (22, 72, 58)
VERD_C = (116, 194, 166)
OCRE = (223, 180, 95)
GRIS = (156, 177, 168)
BLANCO = (255, 255, 255)

W, H = 1200, 630
img = Image.new('RGB', (W, H), FONDO)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 9], fill=VERD_C)

# Logo: casa con pantalla
lx, ly, s = 70, 60, 88
d.rounded_rectangle([lx, ly, lx + s, ly + s], radius=19, fill=VERD)
cx = lx + s / 2
d.line([(lx + 15, ly + 42), (cx, ly + 18), (lx + s - 15, ly + 42)], fill=BLANCO, width=7, joint='curve')
d.rounded_rectangle([lx + 27, ly + 45, lx + s - 27, ly + 68], radius=4, outline=BLANCO, width=5)
d.line([(cx, ly + 68), (cx, ly + 75)], fill=BLANCO, width=5)
d.line([(cx - 12, ly + 75), (cx + 12, ly + 75)], fill=BLANCO, width=5)

d.text((lx + s + 26, ly + 14), NOMBRE, font=fuente(NEGRA, 38), fill=CREMA)
d.text((lx + s + 28, ly + 58), LEMA, font=fuente(NORMAL, 24), fill=GRIS)

d.text((70, 212), 'Voy yo a tu casa', font=fuente(NEGRA, 84), fill=CREMA)
d.text((70, 312), 'Informática a domicilio en La Font de la Figuera', font=fuente(NORMAL, 40), fill=OCRE)

d.text((70, 392), 'Ordenadores · Móviles · Wifi · Impresoras · Virus · Copias de seguridad',
       font=fuente(NORMAL, 25), fill=GRIS)
d.text((70, 428), 'Páginas web · Aplicaciones a medida · Automatización · Inteligencia artificial',
       font=fuente(NORMAL, 25), fill=GRIS)

d.rounded_rectangle([70, 500, 478, 572], radius=12, fill=VERD_C)
d.text((96, 513), TELEFONO, font=fuente(NEGRA, 44), fill=(10, 26, 21))
d.text((512, 524), 'Llama sin compromiso.', font=fuente(NORMAL, 26), fill=CREMA)
img.save('img/portada.png', optimize=True)

ic = Image.new('RGB', (180, 180), VERD)
di = ImageDraw.Draw(ic)
di.line([(34, 88), (90, 42), (146, 88)], fill=BLANCO, width=14, joint='curve')
di.rounded_rectangle([56, 94, 124, 142], radius=8, outline=BLANCO, width=11)
di.line([(90, 142), (90, 154)], fill=BLANCO, width=11)
di.line([(70, 156), (110, 156)], fill=BLANCO, width=11)
ic.save('icono-180.png', optimize=True)
print('img/portada.png e icono-180.png generados')
