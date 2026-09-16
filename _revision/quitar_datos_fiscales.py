#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Versión de prueba de la web: fuera NIF, domicilio, epígrafe del IAE, datos
registrales y la condición de autónomo. Como titular basta el nombre completo.
Los documentos legales se mantienen.

    python _revision/quitar_datos_fiscales.py
"""
import io
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONT = os.path.join(RAIZ, '_contenido')


def cargar(nombre):
    with open(os.path.join(CONT, nombre + '.json'), encoding='utf-8') as fh:
        return json.load(fh)


def guardar(nombre, datos):
    with io.open(os.path.join(CONT, nombre + '.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=1)


def cambiar(lista, indice, contiene, nuevo):
    assert contiene in lista[indice], 'no encuentro %r en %r' % (contiene, lista[indice][:80])
    lista[indice] = nuevo


def quitar(lista, indice, contiene):
    assert contiene in lista[indice], 'no encuentro %r en %r' % (contiene, lista[indice][:80])
    del lista[indice]


def sustituir(texto, viejo, nuevo):
    assert viejo in texto, 'no encuentro %r' % viejo
    return texto.replace(viejo, nuevo)


# ---------------------------------------------------------------------------
# Aviso legal
# ---------------------------------------------------------------------------
a = cargar('legal_aviso')
es = a['secciones'][0]['parrafos']['es']
va = a['secciones'][0]['parrafos']['va']

cambiar(es, 12, 'CÓDIGOS DE CONDUCTA',
        'Adhesión a códigos de conducta: el titular no está adherido a ningún código de conducta.')
cambiar(va, 12, 'CÓDIGOS DE CONDUCTA',
        'Adhesió a codis de conducta: el titular no està adherit a cap codi de conducta.')
quitar(es, 10, 'Registro Mercantil')
quitar(va, 10, 'Registre Mercantil')
quitar(es, 9, 'IAE')
quitar(va, 9, 'IAE')
cambiar(es, 3, 'DOMICILIO PENDIENTE',
        'Ubicación: La Font de la Figuera (Valencia), España.')
cambiar(va, 3, 'DOMICILIO PENDIENTE',
        'Ubicació: la Font de la Figuera (València), Espanya.')
quitar(es, 2, 'NIF')
quitar(va, 2, 'NIF')
cambiar(es, 1, 'trabajador autónomo', 'Titular: Néstor Soriano López.')
cambiar(va, 1, 'treballador autònom', 'Titular: Néstor Soriano López.')

arb_es = a['secciones'][7]['parrafos']['es']
arb_va = a['secciones'][7]['parrafos']['va']
arb_es[4] = sustituir(
    arb_es[4],
    ' [ADHESIÓN AL SISTEMA ARBITRAL DE CONSUMO PENDIENTE DE COMPLETAR: indicar si el titular está adherido o no al Sistema Arbitral de Consumo].',
    ' El titular no está adherido con carácter general al Sistema Arbitral de Consumo, '
    'aunque está dispuesto a valorar en cada caso concreto la propuesta de acudir a él.')
arb_va[4] = sustituir(
    arb_va[4],
    ' [ADHESIÓN AL SISTEMA ARBITRAL DE CONSUMO PENDIENTE DE COMPLETAR: indicar si el titular está adherido o no al Sistema Arbitral de Consumo].',
    " El titular no està adherit amb caràcter general al Sistema Arbitral de Consum, "
    "tot i que està disposat a valorar en cada cas concret la proposta d'acudir-hi.")
a.pop('pendientes', None)
guardar('legal_aviso', a)

# ---------------------------------------------------------------------------
# Condiciones del servicio
# ---------------------------------------------------------------------------
c = cargar('legal_condiciones')
s0 = c['secciones'][0]
s0['parrafos']['es'][0] = sustituir(s0['parrafos']['es'][0],
                                    'Soy autónomo y trabajo solo.', 'Trabajo solo.')
s0['parrafos']['va'][0] = sustituir(s0['parrafos']['va'][0],
                                    'Soc autònom i treballe a soles.', 'Treballe a soles.')
cambiar(s0['lista']['es'], 2, 'DOMICILIO PENDIENTE', 'Ubicación: La Font de la Figuera (Valencia).')
cambiar(s0['lista']['va'], 2, 'DOMICILIO PENDIENTE', 'Ubicació: la Font de la Figuera (València).')
quitar(s0['lista']['es'], 1, 'NIF')
quitar(s0['lista']['va'], 1, 'NIF')
cambiar(s0['lista']['es'], 0, 'trabajador autónomo', 'Titular: Néstor Soriano López.')
cambiar(s0['lista']['va'], 0, 'treballador autònom', 'Titular: Néstor Soriano López.')

form = c['secciones'][8]['lista']
form['es'][0] = sustituir(form['es'][0],
                          ', [DOMICILIO PENDIENTE DE COMPLETAR], 46630 La Font de la Figuera (Valencia).',
                          ', La Font de la Figuera (Valencia).')
form['va'][0] = sustituir(form['va'][0],
                          ', [DOMICILIO PENDIENTE DE COMPLETAR], 46630 la Font de la Figuera (València).',
                          ', la Font de la Figuera (València).')

resp = c['secciones'][10]['lista']
cambiar(resp['es'], 0, 'NIF PENDIENTE', 'Responsable: Néstor Soriano López, La Font de la Figuera.')
cambiar(resp['va'], 0, 'NIF PENDIENTE', 'Responsable: Néstor Soriano López, la Font de la Figuera.')
c.pop('pendientes', None)
guardar('legal_condiciones', c)

# ---------------------------------------------------------------------------
# Política de privacidad
# ---------------------------------------------------------------------------
p = cargar('legal_privacidad')
s0 = p['secciones'][0]
s0['parrafos']['es'][0] = sustituir(s0['parrafos']['es'][0],
                                    'Néstor Soriano López, trabajador autónomo que presta',
                                    'Néstor Soriano López, que presta')
s0['parrafos']['va'][0] = sustituir(s0['parrafos']['va'][0],
                                    'Néstor Soriano López, treballador autònom que presta',
                                    'Néstor Soriano López, que presta')
cambiar(s0['lista']['es'], 2, 'DOMICILIO PENDIENTE', 'Ubicación: La Font de la Figuera (Valencia)')
cambiar(s0['lista']['va'], 2, 'DOMICILIO PENDIENTE', 'Ubicació: la Font de la Figuera (València)')
quitar(s0['lista']['es'], 1, 'NIF')
quitar(s0['lista']['va'], 1, 'NIF')

resp = p['secciones'][11]['lista']
cambiar(resp['es'], 0, 'NIF PENDIENTE', 'Responsable: Néstor Soriano López, La Font de la Figuera.')
cambiar(resp['va'], 0, 'NIF PENDIENTE', 'Responsable: Néstor Soriano López, la Font de la Figuera.')
p.pop('pendientes', None)
guardar('legal_privacidad', p)

# ---------------------------------------------------------------------------
# Comprobación: ni un hueco pendiente ni un dato fiscal propio en ningún JSON
# ---------------------------------------------------------------------------
import glob
import re

prohibido = re.compile(r'PENDIENTE|PENDENT|\bIAE\b|ep[ií]graf|Registro Mercantil|Registre Mercantil|'
                       r'efectos de notificaciones|efectes de notificacions|NIF \[|NIF:|'
                       r'trabajador autónomo|treballador autònom|Soy autónomo|Soc autònom')
fallos = []
for ruta in sorted(glob.glob(os.path.join(CONT, '*.json'))):
    with open(ruta, encoding='utf-8') as fh:
        texto = fh.read()
    json.loads(texto)
    for m in prohibido.finditer(texto):
        fallos.append('%s: %s' % (os.path.basename(ruta), texto[max(0, m.start() - 40):m.end() + 40]))

for nombre in ('legal_aviso', 'legal_condiciones', 'legal_privacidad'):
    d = cargar(nombre)
    for i, sec in enumerate(d['secciones']):
        for campo in ('parrafos', 'lista'):
            if campo in sec and len(sec[campo].get('es', [])) != len(sec[campo].get('va', [])):
                fallos.append('%s seccion %d: %s descuadrado entre es y va' % (nombre, i, campo))

if fallos:
    print('QUEDA ALGO:')
    for f in fallos:
        print('  -', f.replace('\n', ' '))
    raise SystemExit(1)
print('Datos fiscales retirados. Ningun hueco pendiente. es y va cuadran.')
