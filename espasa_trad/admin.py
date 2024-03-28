from django.contrib import admin
from .models import MensajesRecibidos, Error, Flow, Cliente,Key

admin.site.site_header = "Admin Whatsapp BOT"
admin.site.site_title = 'BOT Whatsapp DNogues'
admin.site.index_title = "BOT Whatsapp"

# Register your models here.\\
class MensajesRecibidosAdmin(admin.ModelAdmin):
    list_display=('telefono_cliente','mensaje','creado','id_wa')

class ClienteAdmin(admin.ModelAdmin):
    list_display=('nombre','telefono','email','flow','contacto','cant_contactos','canal_contacto','modelo','comentario','propuesta_crm')
    search_fields = ['nombre','telefono','email','propuesta_crm']
    date_hierarchy = 'contacto'
    ordering = ('-contacto',)

class FlowAdmin(admin.ModelAdmin):
    list_display=('flow_id','respuesta_ok','next_flow','respuesta_nook')

class ErrorAdmin(admin.ModelAdmin):
    list_display=('error','json')

admin.site.register(MensajesRecibidos, MensajesRecibidosAdmin)
admin.site.register(Error,ErrorAdmin)
admin.site.register(Flow,FlowAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Key)

