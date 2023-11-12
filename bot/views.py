from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key, Cliente
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
                telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                try:
                    MensajesRecibidos.objects.get(id_wa=idWA)
                except:
                    try:
                        cliente = Cliente.objects.get(telefono = telefonoCliente)
                    except:
                        cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 0)
                        MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=telefonoCliente,cliente=cliente,telefono_receptor='baires').save()
                        token = Key.objects.get(name='wap')
                        data = services.text_Message('541166531292','Hola')
                        services.enviar_Mensaje_whatsapp(token.token,token.url,data)
                
                
        except json.JSONDecodeError:
            
            Error.objects.create(error='No se pudo decodificar el JSON').save()
            return JsonResponse({"error": "Error al decodificar JSON"}, status=400)

        Error.objects.create(error='OK').save()
