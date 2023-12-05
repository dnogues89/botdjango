import requests
import json
from .key import fransi_key

class FransiCRM():
    def __init__(self,end_point,cliente) -> None:
        self.url = f'https://gvcrmweb.backoffice.com.ar/apicrmfransi/v1/propuesta{end_point}'
        self.api_key = fransi_key
        self.cliente = cliente
        self.data = self.get_data()
        
    def get_data(self):
        data = {
            "referenciaExterna":"1",  #El ID en su sistema, este dato lo voy a usar para controlar que no insertemos duplicados.
            "contacto": {
                "nombre": "", #Obligatorio
                "apellido": "",
                "telefono": "",
                "celular": "",
                "email": "", #Recordá que al menos se debe enviar un dato de contacto
                "dni": "",
                "cuit": ""
            },
            "referencia": "Alaskan", #Obligatorio, la familia, o en su defecto el texto <SIN DEFINIR> o similar.
            "motivoAcercamiento": "whatsapp", #Siempre whatsapp, aunque si envias otro valor, se va a agregar.
            "medioIngreso": "internet", #Siempre internet, idem comentario a motivoAcercamiento.
            "potencial": "", #NO Obligatorio. Acá si evaluas de alguna forma prioridad de caso podes enviar alguno de los siguientes valores: caliente, tibio, frio (o dejar vacio).
            "pagoFinanciado": "",
            "pagoUsado": "", #Valores: si, no. (o dejar vacío)
            "comentarios": "", #cualquier comentario que deje el cliente.
            "ultimaPropuesta": "string"
        }
        
        data['referenciaExterna']=f'{self.cliente.pk}{self.cliente.cant_contactos}'
        
        #Divir el nombre y apellido
        lista = self.cliente.nombre.split(' ')
        if len(lista)>=2:
            data['contacto']['nombre'] = lista[0]
            data['contacto']['apellido'] = ' '.join(lista[1:])
        else:
            data['contacto']['nombre'] = self.cliente.nombre
            
        data['contacto']['celular'] = self.cliente.telefono
        data['contacto']['email'] = self.cliente.email
        data['referencia'] = self.cliente.modelo
        data['comentarios'] = self.cliente.comentario
        data['ultimaPropuesta'] = self.cliente.propuesta_crm
        
        return data

    def send_data(self):
        self.data = json.dumps(self.data)
        headers = {"apiKey": self.api_key, 'Content-Type': 'application/json'}
        response = requests.post(self.url, data=self.data, headers=headers)
        if response.status_code == 200:
            self.cliente.propuesta_crm = response.json()['numero']
            self.cliente.cant_contactos = int(self.cliente.cant_contactos)+1
            self.cliente.save()
            return True, response.json()
        else:
            return False, response.json()

