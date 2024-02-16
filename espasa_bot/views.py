from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import MensajesRecibidos, Error,Key, Cliente, Flow
from django.views.decorators.csrf import csrf_exempt
from . import services
from .salesforce_lead import Salesfroce #Cambiar a Salesforce
import re

from calidad.models import Encuesta

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


#Evitar duplicidad
import threading

# Crear un semáforo para bloquear el acceso al endpoint
lock = threading.Lock()

def endpoint_lock(func):
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper

import json

modelos = {
1:{'modelo':'Amarok','ficha':'https://tinyurl.com/yu9bb7r2'},
2:{'modelo':'Taos','ficha':'https://tinyurl.com/ymm6s7by'},
3:{'modelo':'Polo','ficha':'https://tinyurl.com/ynpot88c'},
4:{'modelo':'Virtus','ficha':'https://tinyurl.com/ynjyrnaq'},
5:{'modelo':'Nivus','ficha':'https://tinyurl.com/ywkl78pg'},
6:{'modelo':'T-Cross','ficha':'https://tinyurl.com/yow85svy'},
7:{'modelo':'Vento','ficha':'https://tinyurl.com/yow85svy'},
8:{'modelo':'Tiguan','ficha':'https://tinyurl.com/yow85svy'},
}

class ChatFlow():
    def __init__(self, cliente, mensaje) -> None:
        self.cliente = cliente
        self.mensaje = mensaje
        self.flow = Flow.objects.get(flow_id=self.cliente.flow)
        self.get_respuesta()
        

    
    def get_respuesta(self):
        hash_map = {
            0:True,
            1:self.validate_numero(len(self.mensaje),30),
            2:self.validate_mail(self.mensaje),
            22:self.validate_numero(self.mensaje,2),
            3:self.validate_numero(self.mensaje,3),
            4:self.validate_numero(self.mensaje,8),
            30:True,
            50:True,
        }
        
        if hash_map[self.flow.flow_id]:
            self.update_cliente()
            self.answer = self.flow.respuesta_ok
            self.answer = self.answer.replace('{self.cliente.nombre}',str(self.cliente.nombre)).replace('{self.cliente.telefono}',str(self.cliente.telefono)).replace('{self.cliente.email}',str(self.cliente.email))
            try:
                self.answer = self.answer.replace('{self.cliente.nombre}',str(self.cliente.nombre)).replace('{self.cliente.telefono}',str(self.cliente.telefono)).replace('{self.cliente.email}',str(self.cliente.email)).replace("{modelos[int(self.mensaje)]['modelo']}",modelos[int(self.mensaje)]['modelo']).replace("{modelos[int(self.mensaje)]['ficha']}",modelos[int(self.mensaje)]['ficha'])
            except:
                pass
            self.cliente.flow=self.flow.next_flow
            self.cliente.save()
        else:
            self.answer = Flow.objects.filter(next_flow=self.flow.flow_id)[0].respuesta_nook

              
    def update_cliente(self):
        if self.flow.flow_id == 0 or self.flow.flow_id == 30:
            try:
                if "|" in self.mensaje:
                    self.cliente.canal_contacto = self.mensaje.split('|')[0]
                if 'mercadolibre.com.ar' in self.mensaje:
                    self.cliente.canal_contacto = 'Mercadolibre'
            except:
                pass
        if self.flow.flow_id == 1:
            self.cliente.nombre = self.mensaje
        if self.flow.flow_id == 2:
            self.cliente.email = self.mensaje
        if self.flow.flow_id == 22:
            if str(self.mensaje) != '1':
                self.cliente.flow = 0
                self.flow = Flow.objects.get(flow_id=0)
        if self.flow.flow_id == 3:
            self.cliente.canal = self.mensaje
            #elegiste taller
            if str(self.mensaje)=='2':
                self.cliente.flow = 222
                self.flow = Flow.objects.get(flow_id=222)
            #elegiste planes
            if str(self.mensaje)=='3':
                self.cliente.flow = 223
                self.flow = Flow.objects.get(flow_id=223)         
        if self.flow.flow_id == 4:
            self.cliente.modelo = modelos[int(self.mensaje)]['modelo']
        #enviar lead al crm
        if self.flow.flow_id == 50:
            if self.cliente.comentario == 'Sin Comentario':
                self.cliente.comentario = self.mensaje
                self.cliente.save()
                send_crm = Salesfroce(self.cliente)
                send_crm = send_crm.send_data()
                self.cliente.cant_contactos = int(self.cliente.cant_contactos)+1
                self.cliente.save()


    def validate_mail(self, correo):
        patron = r'^[A-Za-z0-9\s\._%+-]+@[\w\.-]+\.\w+$'
        if re.match(patron, correo):
            return True
        else:
            return False

    def validate_numero(self,numero,numero_max):
        try:
            numero = int(numero)
            if numero <= numero_max:
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
        return text

    except Exception as e:
        return 'No procesado' + str(e)

# Create your views here.
@csrf_exempt
@endpoint_lock  
def webhook(request):
    # SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.GET.get('hub.verify_token') == "NordelBOT":
            # ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            # SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return HttpResponse("Error de autentificacion.")
    
    if request.method == "POST":    
        data = json.loads(request.body.decode('utf-8'))
        token = Key.objects.get(name='wap')
        
        if data["entry"][0]["changes"][0]['value']['metadata']['phone_number_id'] == token.id_wap:
        
            if 'messages' in data['entry'][0]['changes'][0]['value']:
                if data['entry'][0]['changes'][0]['value']['messages'][0]['type']!='text':
                    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                    telefonoCliente=f'{str(telefonoCliente[3:])}'
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
                        MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='nordel_trad',json=data).save()
                                
                        respuesta = 'Recorda que soy un 🤖 y mi creador no me dio la capacidad de 👀 o👂, pero enviame un *Texto* que estoy para ayudarte. 🦾'
                        data = services.text_Message(telefonoCliente,respuesta)
                        envio = services.enviar_Mensaje_whatsapp(token.token,token.url,data)
                        
            try:  
                if 'messages' in data['entry'][0]['changes'][0]['value']:
                    if data['entry'][0]['changes'][0]['value']['messages'][0]['type']=='text':
                        telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                        telefonoCliente=f'{str(telefonoCliente[3:])}'
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
                            
                            MensajesRecibidos.objects.create(id_wa=idWA,mensaje=mensaje,timestamp=timestamp,telefono_cliente=cliente,telefono_receptor='nordel_trad',json=data).save()
                            chat = ChatFlow(cliente,mensaje)
                            data = services.text_Message(chat.cliente.telefono,chat.answer)
                            envio = services.enviar_Mensaje_whatsapp(token.token,token.url,data)             
                            print(envio)
                            
            except json.JSONDecodeError:
                
                Error.objects.create(error='No se pudo decodificar el JSON').save()
                return JsonResponse({"error": "Error al decodificar JSON"}, status=400)
        return HttpResponse('Hola mundo')
    return HttpResponse('Hola mundo')
    
def clientes_abandonados(request):
    from datetime import datetime, timedelta, timezone
    settings.USE_TZ = False
    # Obtén la zona horaria de Buenos Aires
    now = datetime.now()+timedelta(hours=3)
    limit = datetime.now()+timedelta(hours=3)-timedelta(minutes=30)

    # Obtén la fecha y hora actual en la zona horaria de Buenos Aires
    clientes = Cliente.objects.filter(flow=50)
    
    clientes_filtrados = clientes.filter(contacto__lte=limit)
    
    for cliente in clientes_filtrados:
        cliente.flow = 30
        cliente.comentario = 'Sin Comentario'
        cliente.save()
    
    # Filtra los clientes según tus condiciones
    clientes = Cliente.objects.exclude(flow=50).exclude(flow=0).exclude(flow=30)
    clientes_abandonados = clientes.filter(contacto__lte=limit)
    for cliente in clientes_abandonados:
        send_crm = Salesfroce(cliente) #Cambiar A Salesforce
        send_crm = send_crm.send_data()
        if cliente.email == 'sin@email.com':
            cliente.flow=0
        else:
            cliente.flow = 30
        cliente.cant_contactos = int(cliente.cant_contactos)+1
        cliente.save()
    
    settings.USE_TZ = True
    
    return HttpResponse(f"En espera: {clientes_filtrados}\nAbandonados:{clientes_abandonados}")