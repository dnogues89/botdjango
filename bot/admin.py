from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key

# Register your models here.
class MensajesRecibidosAdmin(admin.ModelAdmin):
    list_display=('cliente','mensaje','creado','id_wa')

admin.site.register(MensajesRecibidos, MensajesRecibidosAdmin)
admin.site.register(Error)
admin.site.register(Flow)
admin.site.register(Cliente)
admin.site.register(Key)

