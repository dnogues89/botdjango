from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key, Cliente, Flow
from django.views.decorators.csrf import csrf_exempt
from . import services
import re



import json
# def enviar_opciones():
#     body = "¡Hola! 👋 Bienvenido a Bigdateros. ¿Cómo podemos ayudarte hoy?"
#     footer = "Equipo Bigdateros"
#     options = ["✅ servicios", "📅 agendar cita"]

#     list = []
#     replyButtonData = services.buttonReply_Message('541166531292', options, body, footer, "sed1",idWA)
#     replyReaction = services.replyReaction_Message('541166531292', idWA, "🫡")
#     list.append(replyReaction)
#     list.append(replyButtonData)
#     for item in list:
#         services.enviar_Mensaje_whatsapp(token.token,token.url,item)

class ChatFlow():
    def __init__(self, cliente, mensaje) -> None:
        self.cliente = cliente
        self.mensaje = mensaje
        self.get_respuesta()
        
    def get_respuesta(self):
        hash_map = {
            0:True,
        }
        
        flow = Flow.objects.get(flow_id=self.cliente.flow)
        if hash_map[flow.flow_id]:
            self.answer = flow.respuesta_ok
            self.cliente.flow=flow.next_flow
            

    def client_flow_by_status(self):
        if self.flow == None or self.status == 0:
            try:
                self.repo.insert_new_client(self.client,self.timestamp)
            except:
                pass

            try:
                modelo = self.msg.split('|')[-1].split('-')[0]
                self.repo.update_client_modelo(self.client,modelo)
                comentario = self.msg.split('|')
                comentario.pop(2)
                print(comentario)
                comentario = ",".join(comentario)
                print(comentario)
                self.repo.update_client_comentario(self.client,comentario)
            except:
                pass

            self.repo.update_client_canal(self.client,3)
            self.repo.update_client_status(self.client,1,self.timestamp)
            self.answer = '🏡¡Hola! Bienvenido a *Espasa AUTO AHORRO* 🚗\n\nUn Asesor Comercial se pondrá en contacto con vos. 👨‍💼\nMientras tanto, te pedimos que nos respondas estas *preguntas* para darte la mejor atención. 🤔\nEn caso que lo necesites, solicitanos una videollamada y te brindamos asesoramiento 100% virtual. 🤳\n*Muchas gracias*\n\n🏷️ ¿Cuál es tu nombre? 🏷️'

        

    def length_check(self,param):
        if len(self.msg) > param:
            self.answer = f'🚫 Por favor que sean menos de {param} caracteres 🚫️'
            return False
        else:
            return True

    def validate_mail(self, correo):
        patron = r'^[A-Za-z0-9\s\._%+-]+@[\w\.-]+\.\w+$'
        if re.match(patron, correo):
            return True
        else:
            return False

    def validate_numero(self,numero):
        try:
            numero = int(numero)
            return True
        except:
            return False
    
def procesar_mensaje(body):
    try:
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
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
        data = json.loads(request.body.decode('utf-8'))
        token = Key.objects.get(name='wap')
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            
            if data['entry'][0]['changes'][0]['value']['messages'][0]['type']!='text':
                telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                telefonoCliente=f'54{str(telefonoCliente[3:])}'
                mensaje='Imagen o Audio'
                idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                try:
                    MensajesRecibidos.objects.get(id_wa=idWA)
                except:
                    try:
                        cliente = Cliente.objects.get(telefono = telefonoCliente)
                    except:
                        cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 0).save()
                    MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='baires',json=data).save()
                    respuesta = 'Recorda que soy un 🤖 y mi creador no me dio la capacidad de 👀 o👂, pero enviame un *Texto* que estoy para ayudarte. 🦾'
                    data = services.text_Message(telefonoCliente,respuesta)
                    services.enviar_Mensaje_whatsapp(token.token,token.url,data)
        try:  
            if 'messages' in data['entry'][0]['changes'][0]['value']:
                if data['entry'][0]['changes'][0]['value']['messages'][0]['type']=='text':
                    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                    telefonoCliente=f'54{str(telefonoCliente[3:])}'
                    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
                    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
                    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
                    try:
                        MensajesRecibidos.objects.get(id_wa=idWA)
                    except:
                        try:
                            cliente = Cliente.objects.get(telefono = telefonoCliente)
                        except:
                            cliente=Cliente.objects.create(telefono = telefonoCliente,flow = 0).save()
                        
                        MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='baires',json=data).save()
                        chat = ChatFlow(cliente,mensaje)
                        data = services.text_Message(chat.cliente.telefono,chat.answer)
                        services.enviar_Mensaje_whatsapp(token.token,token.url,data)             
                        
        except json.JSONDecodeError:
            
            Error.objects.create(error='No se pudo decodificar el JSON').save()
            return JsonResponse({"error": "Error al decodificar JSON"}, status=400)

        Error.objects.create(error='OK',json=data).save()

    return HttpResponse('Hola mundo')