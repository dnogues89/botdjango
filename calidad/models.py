from django.db import models
from bot.models import Cliente

# Create your models here.
class Encuesta(models.Model):
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    entrega = models.DateField(null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    pregunta_1 = models.CharField(max_length=100, null=True, blank=True)
    respuesta_1 = models.CharField(max_length=100, null=True, blank=True)
    pregunta_2 = models.CharField(max_length=100, null=True, blank=True)
    respuesta_2 = models.CharField(max_length=100, null=True, blank=True)
    pregunta_3 = models.CharField(max_length=100, null=True, blank=True)
    respuesta_3 = models.CharField(max_length=100, null=True, blank=True)
    pregunta_4 = models.CharField(max_length=100, null=True, blank=True)
    respuesta_4 = models.CharField(max_length=100, null=True, blank=True)
    pregunta_5 = models.CharField(max_length=100, null=True, blank=True)
    respuesta_5 = models.CharField(max_length=100, null=True, blank=True)