from django.shortcuts import render
from django.http import HttpResponse
import json
from bot.models import Key
from bot import services
from .models import Encuesta

# Create your views here.
def realizar_encuesta(request): 
    encuesta = Encuesta.objects.get(pk=1)
    data = {
   "messaging_product": "whatsapp",
   "to": encuesta.cliente.telefono,
   "type": "template",
   "template": {
       "name": "encuesta_calidad_baires",
       "language": {
           "code": "es_AR",
           "policy": "deterministic"
       },
       "components": [
           {
               "type": "body",
               "parameters": [
                   {
                       "type": "text",
                       "text": encuesta.cliente.nombre
                   },
                   {
                       "type": "text",
                       "text": encuesta.entrega
                   },
                   {
                       "type": "text",
                       "text": encuesta.modelo
                   },
               ]
           },
           {
               "type": "button",
               "sub_type": "quick_reply",
               "index": 0,
               "parameters": [
                   {
                       "type": "text",
                       "text": "Ir a la encuesta"
                   }
               ]
           }
       ]
   }
}
    token = Key.objects.get(name='wap')
    services.enviar_Mensaje_whatsapp(token.token,token.url,data)
    return HttpResponse('Hola mundo')