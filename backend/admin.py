from django.contrib import admin

from .models import (
    Definicion,
    Enciclopedica,
)


# Register your models here.
admin.site.register(Definicion)
admin.site.register(Enciclopedica)
