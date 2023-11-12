from django.db import models

# Create your models here.
class Key(models.Model):
    name = models.CharField(max_length=50)
    url=models.CharField(max_length=100)
    token=models.CharField(max_length=500)


class Error(models.Model):
    error = models.TextField()
    
class Cliente(models.Model):
    telefono = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=50, blank=True,null=True)
    email = models.CharField(max_length=50, blank=True,null=True)
    flow = models.IntegerField(blank=True,null=True)
    modelo = models.CharField(max_length=50, blank=True,null=True)
    canal = models.CharField(max_length=50, blank=True,null=True)
    contacto = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.nombre} | {self.telefono[3:]}'
    
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

    def __str__(self) -> str:
        return self.telefono_cliente
    
    class Meta:
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
    