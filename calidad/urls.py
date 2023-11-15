from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('iniciar/',views.realizar_encuesta, name='iniciar_encuesta' ),
]
