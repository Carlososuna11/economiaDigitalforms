import http
from django.http.response import HttpResponse, JsonResponse,HttpResponseNotFound
from django.shortcuts import render
from django.templatetags.static import static
import json

def formulario(request):
    args= {
        'titulo':'Formulario Reportes EconomiaDigital',
        'titulo_form': 'Por favor, elija 3 activos a reportar'
    }
    try:
        activos = open( 'core/formulario'+ static('formulario/files/activos.txt'),'r')
        lista = list(map(lambda x: x.rstrip('\n'),activos.readlines()))
        activos.close()
        args['activos'] = lista
        # return HttpResponseNotFound("<h1>Pagina No disponible</h1>")
        return render(request,'formulario/formulario.html',args)
    except Exception as ex:
        print(ex)

def respuesta(request):

    archivo = open( 'core/formulario'+ static('formulario/files/resultados.json'),"r")
    data = json.load(archivo)
    archivo.close()
    activos = json.loads(request.body)['activos']
    for activo in activos:
        if activo in data.keys():
            data[activo] += 1
        else:
            data[activo] = 1
    archivo = open( 'core/formulario'+ static('formulario/files/resultados.json'),'w')
    json.dump(data, archivo,indent=4)
    archivo.close()
    data = {
        'ok':'ok'
    }
    return JsonResponse(data,status = http.HTTPStatus.OK)

