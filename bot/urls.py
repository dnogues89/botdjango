from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('webhook/',views.webhook, name='webhook' ),
    path('abandonados/',views.clientes_abandonados, name='abandonados' )
]
