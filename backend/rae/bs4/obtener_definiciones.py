from collections import defaultdict
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from bs4 import BeautifulSoup

from backend.rae.constants import (
    HTTP_HEADERS,
    URL_RAE,
)
from backend.rae.bs4.utils import (
    es_recursiva,
    obtener_acepcion,
    obtener_definiciones_de_frases,
    obtener_especialidades,
    obtener_id_acepcion,
    obtener_ids_sinonimos,
    obtener_metadata,
    obtener_otra_grafia,
    obtener_palabra,
    obtener_regiones,
    tiene_otra_grafia,
)

# Crear una instancia de sesión
session = requests.Session()
# Configurar los reintentos
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[0])
# Crear un adaptador HTTP personalizado
adapter = HTTPAdapter(max_retries=retries)
# Asignar el adaptador a la sesión
session.mount('http://', adapter)
session.mount('https://', adapter)


def obtener_definiciones(palabra):
    # Obtener la response
    response = session.get(f'{URL_RAE}{palabra}', verify=True, headers=HTTP_HEADERS)
    # Obtener el BeautifulSoup de la response
    soup = BeautifulSoup(response.content, 'html.parser')

    palabra = obtener_palabra(soup)
    definiciones_html = soup.find_all('p', {'class': ['j', 'j1', 'j2']})
    definiciones = _armar_definiciones(definiciones_html, palabra)
    todas_las_definiciones = definiciones.copy()

    frases_y_definiciones_html, elemento_padre = obtener_definiciones_de_frases(soup)
    if frases_y_definiciones_html:
        definiciones_de_frases = _armar_definiciones_de_frases(frases_y_definiciones_html, elemento_padre)

        for key, value in definiciones_de_frases.items():
            if key in todas_las_definiciones:
                todas_las_definiciones[key].extend(value)
            else:
                todas_las_definiciones[key] = value

    # Retornar el diccionario
    return todas_las_definiciones


def _armar_definiciones(definiciones_html, palabra):
    definiciones = defaultdict(list)
    for definicion_html in definiciones_html:
        elemento_padre = definicion_html.parent
        # Armar el diccionario por cada definición
        definicion = _armar_definicion(definicion_html, elemento_padre, palabra)
        definiciones[palabra].append(definicion)

        if tiene_otra_grafia(elemento_padre):
            definicion_otra_grafia = obtener_otra_grafia(elemento_padre, palabra, definicion)
            definiciones[definicion_otra_grafia['palabra']].append(definicion_otra_grafia)

    return definiciones


def _armar_definicion(definicion_html, elemento_padre, palabra, es_frase=False):
    c_abbrs = definicion_html.find_all('abbr', {'class': 'c'})
    metadata = obtener_metadata(definicion_html)
    ids_sinonimos = obtener_ids_sinonimos(definicion_html, elemento_padre)

    return {
        'palabra': palabra,
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
            palabra = definicion['palabra']
            definiciones[palabra].append(definicion)

    return definiciones


def _armar_definicion_de_frase(definicion_html, elemento_padre, palabra):
    return _armar_definicion(definicion_html, elemento_padre, palabra, es_frase=True)
