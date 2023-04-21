from django.db import migrations

from backend.models import Definicion
from backend.rae.service import poblar_bd_definiciones

LOTE = 2000


def poblar_definiciones(apps, schema_editor):
    Definicion.objects.all().delete()
    definiciones, elapsed_time = poblar_bd_definiciones()

    definiciones_bd = [
        Definicion(**definicion)
        for definiciones_palabra in definiciones.values()
        for definicion in definiciones_palabra
    ]

    for i in range(0, len(definiciones_bd), LOTE):
        ultima = i + LOTE
        lote_definiciones = definiciones_bd[i:ultima]
        Definicion.objects.bulk_create(lote_definiciones)

    cantidad_de_filas = len(definiciones_bd)
    print(f'{cantidad_de_filas} filas se agregaron a la base de datos. Tiempo: {elapsed_time}s')


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(poblar_definiciones),
    ]
