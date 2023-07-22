from django.db import migrations

from backend.rae.service import poblar_definiciones_en_bd


def poblar_definiciones(apps, schema_editor):
    elapsed_time, definiciones_guardadas = poblar_definiciones_en_bd()

    print(f'Tiempo final: {elapsed_time}s. {definiciones_guardadas} definiciones guardadas')


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(poblar_definiciones),
    ]
