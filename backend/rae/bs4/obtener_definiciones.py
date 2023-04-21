from collections import defaultdict
import requests

from bs4 import BeautifulSoup

from backend.rae.constants import (
    HTTP_HEADERS,
    URL_RAE,
)
from backend.rae.bs4.utils import (
    es_recursiva,
    obtener_acepcion,
    obtener_definiciones_de_frases,
    obtener_definiciones_palabra,
    obtener_especialidades,
    obtener_id_acepcion,
    obtener_ids_sinonimos,
    obtener_metadata,
    obtener_otra_grafia,
    obtener_palabra_rae,
    obtener_palabra_acepcion,
    obtener_regiones,
    tiene_otra_grafia,
)


def obtener_definiciones(palabra):
    """
    1. Obtener la response
    2. Obtener el BeautifulSoup de la response
    3. Por cada definicion:
        1. Armar el diccionario
        2. Agregarlo a la lista
    4. Retornar el diccionario
    """
    # 1. Obtener la response
    response = requests.get(f'{URL_RAE}{palabra}', headers=HTTP_HEADERS)
    # 2. Obtener el BeautifulSoup de la response
    soup = BeautifulSoup(response.content, 'html.parser')

    palabra_rae = obtener_palabra_rae(soup)
    definiciones_html = obtener_definiciones_palabra(soup)
    definiciones = _armar_definiciones(definiciones_html, palabra_rae)

    frases_y_definiciones_html, elemento_padre = obtener_definiciones_de_frases(soup)
    if frases_y_definiciones_html:
        definiciones_de_frases = _armar_definiciones_de_frases(frases_y_definiciones_html, elemento_padre)
        definiciones.update(definiciones_de_frases)
    # 4. Retornar el diccionario

    return definiciones


def _armar_definiciones(definiciones_html, palabra_rae):
    definiciones = defaultdict(list)
    for definicion_html in definiciones_html:
        elemento_padre = definicion_html.parent
        # 3.1. Armar el diccionario por cada definición
        definicion = _armar_definicion(definicion_html, elemento_padre, palabra_rae)
        palabra_acepcion = definicion['palabra_acepcion']
        definiciones[palabra_acepcion].append(definicion)

        if tiene_otra_grafia(elemento_padre):
            definicion_otra_grafia = obtener_otra_grafia(elemento_padre, palabra_acepcion, definicion)
            definiciones[definicion_otra_grafia['palabra_acepcion']].append(definicion_otra_grafia)

    return definiciones


def _armar_definicion(definicion_html, elemento_padre, palabra_rae, es_frase=False):
    c_abbrs = definicion_html.find_all('abbr', {'class': 'c'})
    metadata = obtener_metadata(definicion_html)
    ids_sinonimos = obtener_ids_sinonimos(definicion_html, elemento_padre)

    if es_frase:
        palabra_acepcion = palabra_rae
    else:
        palabra_acepcion = obtener_palabra_acepcion(elemento_padre)

    return {
        'palabra_rae': palabra_rae,
        'palabra_acepcion': palabra_acepcion,
        'especialidad': obtener_especialidades(c_abbrs),
        'region': obtener_regiones(c_abbrs),
        'recursiva': es_recursiva(definicion_html),
        'acepcion': obtener_acepcion(definicion_html),
        'metadata_anterior': metadata['anterior'],
        'metadata_posterior': metadata['posterior'],
        'id_acepcion': obtener_id_acepcion(definicion_html, elemento_padre),
        'id_azul': ids_sinonimos.get('azul'),
        'ids_otros_sinonimos': ids_sinonimos.get('otros_sinonimos'),
        'es_frase': es_frase,
    }


def _armar_definiciones_de_frases(frases_y_definiciones_html, elemento_padre):
    definiciones = defaultdict(list)
    for frase, definiciones_html in frases_y_definiciones_html.items():
        for definicion_html in definiciones_html:
            definicion = _armar_definicion_de_frase(definicion_html, elemento_padre, frase)
            palabra_acepcion = definicion['palabra_acepcion']
            definiciones[palabra_acepcion].append(definicion)

    return definiciones


def _armar_definicion_de_frase(definicion_html, elemento_padre, palabra_rae):
    return _armar_definicion(definicion_html, elemento_padre, palabra_rae, es_frase=True)
