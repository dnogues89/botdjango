from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def webhook(request):
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "FransiBOT":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return "Error de autentificacion."
    
    return JsonResponse({"asd":"asd"})