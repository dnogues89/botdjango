from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error

import json


# Create your views here.

def webhook(request):
    # SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.GET.get('hub.verify_token') == "FransiBOT":
            # ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            # SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return HttpResponse("Error de autentificacion.")
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        if data['entry'][0]['changes'][0]['value']['messages'][0]['type']=='text':
            #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
            telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            #EXTRAEMOS EL TELEFONO DEL CLIENTE
            mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
            idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
            #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
            timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
            MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=telefonoCliente,telefono_receptor='baires').save()
            
    except json.JSONDecodeError:
        
            # Error.objects.create(error='No se pudo decodificar el JSON').save()
        return JsonResponse({"error": "Error al decodificar JSON"}, status=400)

    Error.objects.create(error='OK').save()

    return HttpResponse("ACA")
