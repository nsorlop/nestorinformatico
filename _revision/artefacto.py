#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara una copia de la web para publicarla como vista previa.

La página principal se entrega sin las etiquetas <html>, <head> y <body>,
porque el publicador ya pone ese envoltorio, y con el CSS metido dentro.
El resto de páginas van tal cual, como ficheros que acompañan.

    python _revision/artefacto.py
"""
import os
import re
import shutil

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, '_artefacto')


def leer(ruta):
    with open(os.path.join(RAIZ, ruta), encoding='utf-8') as fh:
        return fh.read()


def main():
    if os.path.isdir(SALIDA):
        shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)

    html = leer('index.html')

    titulo = re.search(r'<title>(.*?)</title>', html, re.S)
    titulo = titulo.group(1).strip() if titulo else 'Néstor el Informático'

    cuerpo = re.search(r'<body>(.*)</body>', html, re.S).group(1).strip()

    # El CSS va dentro de la página para que no dependa del orden de carga
    css = leer('css/fuentes.css') + '\n' + leer('css/estilos.css')
    # Las rutas de las fuentes dejan de ser relativas a /css
    css = css.replace("url('../fonts/", "url('fonts/")

    # Los datos estructurados de la cabecera se conservan
    jsonld = re.findall(r'<script type="application/ld\+json">.*?</script>', html, re.S)

    partes = ['<title>%s</title>' % titulo,
              '<style>\n%s\n</style>' % css]
    partes += jsonld
    partes.append(cuerpo)

    with open(os.path.join(SALIDA, 'portada.html'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(partes))

    # Ficheros que acompañan a la página.
    # La portada de castellano NO va aquí: es la página principal y se sirve en
    # la raíz, así que los enlaces que apuntan a index.html hay que reescribirlos.
    acompanan = ['va/index.html']
    for nombre in ('servicios.html', 'precios.html', 'sobre-mi.html',
                   'preguntas.html', 'contacto.html', 'legal.html'):
        acompanan.append(nombre)
        acompanan.append('va/' + nombre)
    acompanan += ['css/estilos.css', 'css/fuentes.css', 'js/app.js',
                  'img/portada.png', 'favicon.svg']
    acompanan += ['fonts/' + f for f in sorted(os.listdir(os.path.join(RAIZ, 'fonts')))]

    total = 0
    for rel in acompanan:
        origen = os.path.join(RAIZ, rel)
        destino = os.path.join(SALIDA, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if rel.endswith('.html'):
            texto = leer(rel)
            # Solo las paginas de la raiz: su index.html es la pagina principal
            # del artefacto y se sirve en la raiz, no como fichero aparte.
            # Las de va/ apuntan a va/index.html, que si se publica tal cual.
            if '/' not in rel:
                texto = texto.replace('href="index.html"', 'href="./"')
            else:
                # Desde va/, el enlace al castellano tiene que ir a la raiz
                texto = texto.replace('href="../index.html"', 'href="../"')
            with open(destino, 'w', encoding='utf-8', newline=chr(10)) as fh:
                fh.write(texto)
        else:
            shutil.copy2(origen, destino)
        total += os.path.getsize(destino)

    principal = os.path.getsize(os.path.join(SALIDA, 'portada.html'))
    print('portada.html      %7d bytes' % principal)
    print('ficheros extra    %7d (%.0f KB en total)' % (len(acompanan), total / 1024))
    print('carpeta           %s' % SALIDA)


if __name__ == '__main__':
    main()
