from django.db import models

# Create your models here.
class MensajesRecibidos(models.Model):
    id_wa = models.CharField(max_length=100, unique=True)
    mensaje = models.TextField()
    timestamp = models.IntegerField()
    telefono_cliente = models.CharField(max_length=100)
    telefono_receptor = models.CharField(max_length=100)
    
