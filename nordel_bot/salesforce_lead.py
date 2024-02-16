import requests
import json
from django.core.mail import send_mail


class Salesfroce():
    def __init__(self, cliente) -> None:
        self.cliente = cliente
        self.get_data()
        

    def get_data(self):
        self.apellido = self.cliente.nombre
        self.email = self.cliente.email
        self.telefono = self.cliente.telefono
        self.comentario = self.cliente.comentario
        self.producto = self.cliente.modelo
        self.canal = self.cliente.canal_contacto
    
    def send_data(self):
        from_mail='pybotwhat@gmail.com'
        asunto = 'Salesforce Web2Lead'
        mensaje = f"""
            Nombre: \n
            Apellido: {self.apellido}\n
            Email: {self.email}\n
            Teléfono: {self.telefono}\n
            Origen: {self.canal}\n
            Concesionario: 3101 - NORDELBAHN\n
            Campaña: \n
            Comentario: {self.comentario}\n
            País:\n
            Provincia:\n
            Localidad:\n
            Código Postal:\n
            Producto: {self.producto}\n
            """
        send_mail(asunto,mensaje,from_mail,['vw_emailtoleadservice@j-27sndpfxzeziihub3wz3ki0i9mngk47qm2qzpyudikkis5wmj3.f2-1j2mfeak.na173.apex.salesforce.com','mkt1@nordelbahn.com.ar'])
