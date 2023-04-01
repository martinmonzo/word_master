from django.contrib import admin

from .models import (
    Definition,
    Encyclopedic,
)


# Register your models here.
admin.site.register(Definition)
admin.site.register(Encyclopedic)
