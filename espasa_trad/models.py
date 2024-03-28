from django.db import models

# Create your models here.
class Key(models.Model):
    name = models.CharField(max_length=50,help_text="Poner wap, para token de meli, sales para salesforce")
    url=models.CharField(max_length=100,help_text="Url de WAP, o 3 siglas de origen salesforce")
    token=models.CharField(max_length=500,help_text="Va el token de wap, o el concesionario")
    id_wap = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    


class Error(models.Model):
    error = models.TextField()
    json = models.JSONField()
    
class Cliente(models.Model):
    telefono = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True,null=True, default="Estimado")
    email = models.CharField(max_length=50, blank=True,null=True, default='sin@email.com')
    flow = models.IntegerField(blank=True,null=True)
    modelo = models.CharField(max_length=50, blank=True,null=True,default='Sin especificar')
    canal = models.CharField(max_length=50, blank=True,null=True)
    comentario = models.CharField(max_length=1000,blank=True,null=True,default='Sin Comentario')
    contacto = models.DateTimeField(auto_now=True)
    propuesta_crm = models.CharField(max_length=20, blank=True, null=True, default="",verbose_name='Pub Meli')
    canal_contacto = models.CharField(max_length=100,blank=True,null=True, default='WAP')
    cant_contactos = models.IntegerField(default=0)
    # pub_meli = models.CharField(max_length=100,blank=True,null=True, default='')
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        
    
    
class Flow(models.Model):
    flow_id = models.IntegerField()
    respuesta_ok = models.TextField()
    next_flow = models.IntegerField(blank=True,null=True)
    respuesta_nook = models.TextField(blank=True,null=True)
    
class MensajesRecibidos(models.Model):
    id_wa = models.CharField(max_length=100, unique=True)
    mensaje = models.TextField()
    timestamp = models.IntegerField()
    telefono_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    telefono_receptor = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_now_add=True)
    json = models.JSONField(blank=True)
    
    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
    