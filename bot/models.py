from django.db import models

# Create your models here.
class MensajesRecibidos(models.Model):
    id_wa = models.CharField(max_length=100, unique=True)
    mensaje = models.TextField()
    timestamp = models.IntegerField()
    telefono_cliente = models.CharField(max_length=100)
    telefono_receptor = models.CharField(max_length=100)
    creado = models.DateTimeField(auto_created=True)

    def __str__(self) -> str:
        return self.telefono_cliente
    
    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
    
class Error(models.Model):
    error = models.TextField()
    
class Cliente(models.Model):
    telefono = models.IntegerField()
    nombre = models.CharField(max_length=50, blank=True,null=True)
    email = models.CharField(max_length=50, blank=True,null=True)
    flow = models.IntegerField(blank=True,null=True)
    modelo = models.CharField(max_length=50, blank=True,null=True)
    canal = models.CharField(max_length=50, blank=True,null=True)
    contacto = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f''
    
    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
    
class Flow(models.Model):
    flow_id = models.IntegerField()
    respuesta = models.TextField()