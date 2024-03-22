from django.contrib import admin
from django.urls import path

from . import views
from espasa_trad.views import webhook, clientes_abandonados

urlpatterns = [
    path('webhook/',views.webhook, name='webhook' ),
    path('abandonados/',views.clientes_abandonados, name='abandonados' ),
    path('webhook_trad/',webhook, name='webhook_trad' ),
    path('abandonados_trad/',clientes_abandonados, name='abandonados_trad' )
]
