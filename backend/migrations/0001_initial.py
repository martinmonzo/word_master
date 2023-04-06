# Generated by Django 4.1.7 on 2023-04-06 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Definicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acepcion', models.TextField()),
                ('respuesta', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=100, null=True)),
                ('categoria_gramatical', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100, null=True)),
                ('es_facil', models.BooleanField(default=False)),
                ('es_muy_dificil', models.BooleanField(default=False)),
                ('archivo', models.CharField(max_length=100, null=True)),
                ('otra_categoria', models.CharField(max_length=100, null=True)),
                ('coloquial', models.BooleanField()),
                ('uso', models.CharField(max_length=10, null=True)),
                ('descripcion_final', models.CharField(max_length=100, null=True)),
                ('recursiva', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Enciclopedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('respuesta', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=100)),
                ('subcategoria', models.CharField(max_length=100)),
                ('es_facil', models.BooleanField(default=False)),
                ('es_muy_dificil', models.BooleanField(default=False)),
            ],
        ),
    ]
