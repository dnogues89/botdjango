from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key

# Register your models here.
admin.site.register(MensajesRecibidos)
admin.site.register(Error)
admin.site.register(Flow)
admin.site.register(Cliente)
admin.site.register(Key)

