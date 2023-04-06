from django.db import models

# Create your models here.
class Definicion(models.Model):
    acepcion = models.TextField()
    respuesta = models.CharField(max_length=255)
    region = models.CharField(max_length=100, null=True) 
    categoria_gramatical = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, null=True)
    es_facil = models.BooleanField(default=False)
    es_muy_dificil = models.BooleanField(default=False)
    archivo = models.CharField(max_length=100, null=True)
    otra_categoria = models.CharField(max_length=100, null=True)
    coloquial = models.BooleanField()
    uso = models.CharField(max_length=10, null=True)
    descripcion_final = models.CharField(max_length=100, null=True)
    recursiva = models.BooleanField()


class Enciclopedica(models.Model):
    descripcion = models.TextField()
    respuesta = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    subcategoria = models.CharField(max_length=100)
    es_facil = models.BooleanField(default=False)
    es_muy_dificil = models.BooleanField(default=False)
