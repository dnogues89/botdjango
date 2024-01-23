import requests
import json
from .key import fransi_key
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
    
    def send_data(self):
        from_mail='pybotwhat@gmail.com'
        asunto = 'Salesforce Web2Lead'
        mensaje = f"""
            Nombre: \n
            Apellido: {self.apellido}\n
            Email: {self.email}\n
            Teléfono: {self.telefono}\n
            Origen: WAT\n
            Concesionario: 3046 - ESPASA S.A.\n
            Campaña: \n
            Comentario: {self.comentario}\n
            País:\n
            Provincia:\n
            Localidad:\n
            Código Postal:\n
            Producto: {self.producto}\n
            """
        send_mail(asunto,mensaje,from_mail,['damiannogues@icloud.com'])
