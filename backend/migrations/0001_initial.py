# Generated by Django 4.2.3 on 2023-07-18 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Definicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('palabra', models.CharField(max_length=255)),
                ('especialidad', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('recursiva', models.BooleanField()),
                ('acepcion', models.TextField()),
                ('metadata_anterior', models.CharField(max_length=255)),
                ('metadata_posterior', models.CharField(max_length=255)),
                ('id_acepcion', models.CharField(max_length=20)),
                ('id_azul', models.CharField(blank=True, max_length=20, null=True)),
                ('ids_otros_sinonimos', models.TextField(blank=True, null=True)),
                ('es_frase', models.BooleanField()),
                ('es_facil', models.BooleanField(default=False)),
                ('es_muy_dificil', models.BooleanField(default=False)),
                ('archivo', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Definiciones',
            },
        ),
        migrations.CreateModel(
            name='Enciclopedica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('respuesta', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=100)),
                ('subcategoria', models.CharField(max_length=100)),
                ('es_facil', models.BooleanField(default=False)),
                ('es_muy_dificil', models.BooleanField(default=False)),
                ('archivo', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
