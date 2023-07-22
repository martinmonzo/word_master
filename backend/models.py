from django.db import models

# Create your models here.
class Definicion(models.Model):
    id = models.AutoField(primary_key=True)
    palabra = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True) 
    recursiva = models.BooleanField()
    acepcion = models.TextField()
    metadata_anterior = models.CharField(max_length=255)
    metadata_posterior = models.CharField(max_length=255)
    id_acepcion = models.CharField(max_length=20)
    id_azul = models.CharField(max_length=20, null=True, blank=True)
    ids_otros_sinonimos = models.TextField(null=True, blank=True)
    es_frase = models.BooleanField()

    es_facil = models.BooleanField(default=False)
    es_muy_dificil = models.BooleanField(default=False)
    archivo = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Definiciones"


class Enciclopedica(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    respuesta = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=100)
    es_facil = models.BooleanField(default=False)
    es_muy_dificil = models.BooleanField(default=False)
    archivo = models.CharField(max_length=100, null=True)
