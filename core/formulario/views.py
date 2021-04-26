import io
import http
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,reverse
from django.templatetags.static import static
import json
import os
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import *
import ast
from django.contrib.auth import authenticate,login

@ensure_csrf_cookie
def formulario(request):
    args= {
        'titulo':'Formulario Reportes EconomiaDigital',
        'titulo_form': 'Por favor, elija 3 activos a reportar'
    }
    try:
        activos = open(os.path.join(os.path.dirname(__file__),'static','formulario','files','activos.txt'),'r')
        lista = list(map(lambda x: x.rstrip('\n'),activos.readlines()))
        activos.close()
        args['activos'] = lista
        # return HttpResponseNotFound("<h1>Pagina No disponible</h1>")
        return render(request,'formulario/formulario.html',args)
    except Exception as ex:
        print(ex)

def respuesta(request):
    try:
        formulario = Resultados.objects.get(pk=1)
        data = ast.literal_eval(formulario.formulario)
        activos = json.loads(request.body)['activos']
        for activo in activos:
            if activo in data.keys():
                data[activo] += 1
            else:
                data[activo] = 1
        formulario.formulario = data
        formulario.save()
        data = {
            'ok':'ok'
        }
        return JsonResponse(data,status = http.HTTPStatus.OK)
    except Exception as ex:
        print(ex)
    
@ensure_csrf_cookie
def obtener_resultados(request):
    args = dict()
    args['titulo'] = 'Reportar Pago Manual'
    return render(request,'formulario/obtener_resultados.html')

def procesar_solicitud(request):
    data = json.loads(request.body)
    user = authenticate(request,username=data['usuario'], password=data['password'])
    if user is not None:
        if user.is_active:
            login(request,user)
            
            # bot = telebot.TeleBot("1735544352:AAGy9o3qyIgojGYRBCXqWqVBWgcOgZt-l9s")
            # bot.send_document('1642361652',txt)
            data = {
                'ok': "ok"
            }
            return JsonResponse(data,status = http.HTTPStatus.OK)
    data = {
        'Error': "Error"
    }
    return JsonResponse(data,status = http.HTTPStatus.OK)

@login_required
def resultados(request):
    formulario = Resultados.objects.get(pk=1)
    info = ast.literal_eval(formulario.formulario)
    info = dict(sorted(info.items(), key=lambda item: item[1],reverse=True))
    args = dict()
    args['resultados'] = info
    return render(request,'formulario/resultados.html',args)


@login_required
def delete_results(request):
    data = json.loads(request.body)
    formulario = Resultados.objects.get(pk=data['pk'])
    formulario.formulario = "{}"
    formulario.save()
    data = {
                'ok': "ok"
            }
    return JsonResponse(data,status = http.HTTPStatus.OK)