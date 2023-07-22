from concurrent.futures import as_completed, ThreadPoolExecutor
import time

from backend.models import Definicion
from backend.rae.bs4.obtener_definiciones import obtener_definiciones

CANTIDAD_LOTE = 2000


def poblar_definiciones_en_bd():
    """
    Recorre todas las palabras del listado, obtiene la definición de cada una
    en dle.rae.es/{palabra} y lo guarda en la base de datos.
    """
    start_time = time.perf_counter()
    palabras_guardadas = 0

    Definicion.objects.all().delete()
    with open('backend/rae/listado_palabras.txt', 'r') as listado_palabras:
        palabras = listado_palabras.readlines()
        with ThreadPoolExecutor(max_workers=16) as executor:
            for i in range(0, len(palabras), CANTIDAD_LOTE):
                lote = palabras[i:i+CANTIDAD_LOTE]
                futures = [
                    executor.submit(obtener_definiciones, palabra)
                    for palabra in lote
                    if (not palabra.endswith('-') and not palabra.startswith('-') and not ' ' in palabra)
                ]

                for future in as_completed(futures):
                    definiciones = future.result()
                    guardar_definiciones(definiciones)
                    palabras_guardadas += len(definiciones)

                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                print(f'{palabras_guardadas} palabras guardadas. Tiempo: {elapsed_time}s')
                time.sleep(5)

    definiciones_guardadas = Definicion.objects.count()
    return elapsed_time, definiciones_guardadas


def guardar_definiciones(definiciones):
    definiciones_bd = [
        Definicion(**definicion)
        for definiciones_palabra in definiciones.values()
        for definicion in definiciones_palabra
    ]

    Definicion.objects.bulk_create(definiciones_bd)
