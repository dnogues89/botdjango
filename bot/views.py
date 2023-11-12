from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key
from django.views.decorators.csrf import csrf_exempt
from . import services



import json

def procesar_mensaje(body):
    try:
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = services.replace_start(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)
        return 'procesado'

    except Exception as e:
        return 'No procesado' + str(e)


# Create your views here.
@csrf_exempt
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
    
    if request.method == "POST":    
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
                token = Key.objects.get(name='wap')
                data = services.text_Message(MensajesRecibidos.telefono_cliente,'Hola')
                services.enviar_Mensaje_whatsapp(token.token,token.url,data)
                
                
        except json.JSONDecodeError:
            
            Error.objects.create(error='No se pudo decodificar el JSON').save()
            return JsonResponse({"error": "Error al decodificar JSON"}, status=400)

        Error.objects.create(error='OK').save()
