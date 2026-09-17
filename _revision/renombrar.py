#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica el nombre definitivo y la dirección de GitHub Pages.

    Castellano: Néstor el Informático
    Valenciano: Néstor l'Informàtic
    Web:        https://nestorinformatico.es/

Cuando el dominio propio esté apuntado, basta con cambiar URL_NUEVA y volver a
ejecutar este script y python build.py.
"""
import io
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

MARCA_ES = 'Néstor el Informático'
MARCA_VA = "Néstor l'Informàtic"
URL_VIEJA = re.compile(r'https://nsorlop\.github\.io/(?:informatica|web-informatica|nestorinformatico)/')
URL_NUEVA = 'https://nestorinformatico.es/'


def leer(ruta):
    with io.open(ruta, encoding='utf-8') as fh:
        return fh.read()


def escribir(ruta, texto):
    with io.open(ruta, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(texto)


cambios = []

# 1. build.py: diccionario NEGOCIO
s = leer('build.py')
s2 = s.replace("'marca':        'Informática Néstor',", "'marca':        '%s'," % MARCA_ES)
s2 = s2.replace("'marca_va':     'Informàtica Néstor',", "'marca_va':     \"%s\"," % MARCA_VA)
s2 = URL_VIEJA.sub(URL_NUEVA, s2)
assert s2 != s, 'build.py sin cambios'
escribir('build.py', s2)
cambios.append('build.py')

# 2. marca.json: nombre recomendado
p = '_contenido/marca.json'
d = json.loads(leer(p))
d['nombre']['recomendado'] = {'es': MARCA_ES, 'va': MARCA_VA}
escribir(p, json.dumps(d, ensure_ascii=False, indent=1))
cambios.append(p)

# 3. seo.json: nombre en los datos estructurados de Google
p = '_contenido/seo.json'
d = json.loads(leer(p))
d['jsonld']['name'] = MARCA_ES
d['jsonld']['alternateName'] = MARCA_VA
texto = URL_VIEJA.sub(URL_NUEVA, json.dumps(d, ensure_ascii=False, indent=1))
escribir(p, texto)
cambios.append(p)

# 4. Dirección de la web dentro de los textos legales y de la documentación
for p in ('_contenido/legal_aviso.json', '_contenido/legal_condiciones.json',
          '_contenido/legal_privacidad.json', 'README.md', 'LANZAMIENTO.md'):
    t = leer(p)
    t2 = URL_VIEJA.sub(URL_NUEVA, t)
    if t2 != t:
        escribir(p, t2)
        cambios.append(p)

# 5. README: título y URL del repositorio
t = leer('README.md')
t = t.replace('# Informática Néstor · web del servicio a domicilio',
              '# Néstor el Informático · web del servicio a domicilio')
t = t.replace('https://github.com/nsorlop/informatica.git',
              'https://github.com/nsorlop/nestorinformatico.git')
escribir('README.md', t)

# 6. Preparación de la vista previa
t = leer('_revision/artefacto.py')
escribir('_revision/artefacto.py', t.replace("'Informática Néstor'", "'%s'" % MARCA_ES))

# Comprobación: no puede quedar ni el nombre ni la dirección antiguos
restos = []
for raiz, dirs, ficheros in os.walk('.'):
    if any(x in raiz for x in ('_artefacto', '.git', 'fonts', '__pycache__')):
        continue
    for f in ficheros:
        if f.endswith(('.json', '.py', '.md')) and f != 'renombrar.py':
            ruta = os.path.join(raiz, f)
            t = leer(ruta)
            if 'Informática Néstor' in t or 'Informàtica Néstor' in t or URL_VIEJA.search(t):
                restos.append(ruta)
for json_ in ('_contenido/marca.json', '_contenido/seo.json', '_contenido/legal_aviso.json',
              '_contenido/legal_condiciones.json', '_contenido/legal_privacidad.json'):
    json.loads(leer(json_))
print('Ficheros cambiados:', ', '.join(cambios))
print('Restos del nombre o la URL antiguos:', restos or 'ninguno')
