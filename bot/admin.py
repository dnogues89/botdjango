from django.contrib import admin
from .models import MensajesRecibidos, Error

# Register your models here.
admin.site.register(MensajesRecibidos)
admin.site.register(Error)