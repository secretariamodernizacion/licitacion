from django.db import connections
from django.http import JsonResponse
from base.models import Institucion, Respuesta
from django.db.models import Sum

from datetime import datetime


def informe(request, codigo_dipres):
    return JsonResponse({'url': 'asd'})


def canal_preferencia(request, pk=None):

    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    # labels = ['pec_canal_telefono', 'pec_canal_web', 'pec_canal_presencial']
    # MK recomendó ocupar pec_Eval los que tengan dato en vez que pec_Canal
    labels = ['pec_eval_telefono', 'pec_eval_web', 'pec_eval_presencial']

    data = []
    labels_with_data = []
    resp_anio = respuestas.filter(anio=anio)
    total = resp_anio.count()
    for label in labels:
        porcentaje = round(resp_anio.filter(**{label + '__isnull': False}).count() / total * 100, 0)
        if porcentaje > 0:
            labels_with_data.append(label)
            data.append(porcentaje)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def canal_evaluacion(request, pk=None):

    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pec_eval_telefono', 'pec_eval_web', 'pec_eval_presencial']
    # labels = ['pec_eval_telefono']

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    anios = ["2016", "2017", "2018", "2019", "2020"]

    datasets = []
    for anio in anios:
        resp_anio = respuestas.filter(anio=anio)
        if resp_anio.count() == 0:
            continue

        datasets.append({'label': 'Satisfecho', 'data': [], 'stack': anio, 'backgroundColor': '#00d1b2', })
        datasets.append({'label': 'Neutro', 'data': [], 'stack': anio, 'backgroundColor': '#FBD561', })
        datasets.append({'label': 'Insatisfecho', 'data': [], 'stack': anio, 'backgroundColor': '#F08289', })

        for label in labels:
            insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
            satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

            total = insatisfecho_sum + neutro_sum + satisfecho_sum
            # if total and total >= 0:
            #     labels_with_data.append(label)
            for dataset in datasets:
                if dataset.get("label") == 'Satisfecho' and dataset.get("stack") == anio:
                    dataset["data"].append(round(satisfecho_sum / total * 100))

            for dataset in datasets:
                if dataset.get("label") == 'Neutro' and dataset.get("stack") == anio:
                    dataset["data"].append(round(neutro_sum / total * 100))

            for dataset in datasets:
                if dataset.get("label") == 'Insatisfecho' and dataset.get("stack") == anio:
                    dataset["data"].append(round(insatisfecho_sum / total * 100))

        print(datasets)

    if len(datasets) > 6:
        datasets = datasets[-6:]

    return JsonResponse({'labels': labels, 'datasets': datasets}, safe=False)


def data_atributos(request, pk=None):
    print(datetime.now())
    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pev_tram_facil', 'pev_tram_tiempo', 'pev_tram_claridad_pasos', 'pev_tram_info_compr',
              'pev_tram_info_util', 'pev_tram_resp_util', 'pev_tram_resp_compl', 'pev_tram_resp_clara', 'pev_tram_acogido', ]

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    efectivo_para_ordenar = []
    labels_with_data = []
    resp_anio = respuestas.filter(anio=anio)
    for label in labels:
        insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        total = insatisfecho_sum + neutro_sum + satisfecho_sum
        if total and total >= 0:
            labels_with_data.append(label)
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))
            efectivo_para_ordenar.append(round(satisfecho_sum / total * 100) - round(insatisfecho_sum / total * 100))

    ordenado = sorted(range(len(efectivo_para_ordenar)), key=lambda k: efectivo_para_ordenar[k])
    labels_with_data = ordenar(labels_with_data, ordenado)
    data["insatisfecho"] = ordenar(data["insatisfecho"], ordenado)
    data["neutro"] = ordenar(data["neutro"], ordenado)
    data["satisfecho"] = ordenar(data["satisfecho"], ordenado)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


import copy


def ordenar(arreglo, ordenado):
    temp = copy.deepcopy(arreglo)
    for (i, v) in enumerate(ordenado):
        temp[i] = arreglo[v]

    return temp


def data_imagen(request, pk=None):
    respuestas = Respuesta.objects.all()
    anio = 2020

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anio = institucion.datos.get("anios")[-1]

    labels = ['pi_imagen_transp', 'pi_imagen_preocupa', 'pi_imagen_actual', 'pi_imagen_funcion', 'pi_imagen_satisface']

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    resp_anio = respuestas.filter(anio=anio)
    labels_with_data = []
    efectivo_para_ordenar = []
    for label in labels:
        insatisfecho_sum = resp_anio.filter(**{label + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{label + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{label + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        total = insatisfecho_sum + neutro_sum + satisfecho_sum
        if total and total >= 0:
            labels_with_data.append(label)
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))
            efectivo_para_ordenar.append(round(satisfecho_sum / total * 100) - round(insatisfecho_sum / total * 100))

    ordenado = sorted(range(len(efectivo_para_ordenar)), key=lambda k: efectivo_para_ordenar[k])
    labels_with_data = ordenar(labels_with_data, ordenado)
    data["insatisfecho"] = ordenar(data["insatisfecho"], ordenado)
    data["neutro"] = ordenar(data["neutro"], ordenado)
    data["satisfecho"] = ordenar(data["satisfecho"], ordenado)

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def data_dimension(request, pk=None):
    respuestas = Respuesta.objects.all()

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)

    medicion = request.GET.get("medicion", 'experiencia')

    # esto debería salir
    if medicion == 'tipo_tramite':
        medicion = 'experiencia'

    dimension = request.GET.get("dimension", 'anio')
    labels = [d[dimension] for d in respuestas.values(dimension).distinct(dimension) if d[dimension]]
    if dimension == 'tipo_tramite':
        labels = [l for l in labels if l != 'Otros']

    labels.append('Todos')

    if request.GET.get("edad"):
        respuestas = respuestas.filter(edad=request.GET.get("edad").replace("_", " "))

    if request.GET.get("sexo"):
        respuestas = respuestas.filter(sexo=request.GET.get("sexo"))

    if request.GET.get("educacion"):
        respuestas = respuestas.filter(educacion=request.GET.get("educacion"))

    if request.GET.get("habilitado"):
        respuestas = respuestas.filter(habilitado=request.GET.get("habilitado"))

    if request.GET.get("anio"):
        respuestas = respuestas.filter(anio=request.GET.get("anio"))

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }
    labels_with_data = []

    for label in labels:
        if label == 'Todos':
            resp_anio = respuestas
        else:
            resp_anio = respuestas.filter(**{dimension: label})

        insatisfecho_sum = resp_anio.filter(**{medicion + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{medicion + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{medicion + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        total = insatisfecho_sum + neutro_sum + satisfecho_sum
        if total > 0:
            labels_with_data.append(label)

            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))

    return JsonResponse({'labels': labels_with_data, 'data': data}, safe=False)


def data_grafica(request, pk=None):
    print(datetime.now())
    respuestas = Respuesta.objects.all()
    anios = [2016, 2017, 2018, 2019, 2020]

    if pk:
        institucion = Institucion.objects.get(pk=pk)
        respuestas = respuestas.filter(institucion=institucion)
        anios = institucion.datos.get("anios")

    medicion = request.GET.get("medicion", 'experiencia')

    if request.GET.get("edad"):
        respuestas = respuestas.filter(edad=request.GET.get("edad").replace("_", " "))

    if request.GET.get("sexo"):
        respuestas = respuestas.filter(sexo=request.GET.get("sexo"))

    if request.GET.get("educacion"):
        respuestas = respuestas.filter(educacion=request.GET.get("educacion"))

    if request.GET.get("habilitado"):
        respuestas = respuestas.filter(habilitado=request.GET.get("habilitado"))

    data = {
        'insatisfecho': [],
        'neutro': [],
        'satisfecho': []
    }

    for anio in anios:
        # if anio == 2019:
        #     import ipdb
        #     ipdb.set_trace()
        resp_anio = respuestas.filter(anio=anio)
        insatisfecho_sum = resp_anio.filter(**{medicion + '__in': [1, 2, 3, 4]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        neutro_sum = resp_anio.filter(**{medicion + '__in': [5]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0
        satisfecho_sum = resp_anio.filter(**{medicion + '__in': [6, 7]}).aggregate(Sum('f_pond'))["f_pond__sum"] or 0

        total = insatisfecho_sum + neutro_sum + satisfecho_sum
        if total == 0:
            data["insatisfecho"].append(None)
            data["neutro"].append(None)
            data["satisfecho"].append(None)
        else:
            data["insatisfecho"].append(round(insatisfecho_sum / total * 100))
            data["neutro"].append(round(neutro_sum / total * 100))
            data["satisfecho"].append(round(satisfecho_sum / total * 100))

    print(datetime.now())
    return JsonResponse({'labels': anios, 'data': data}, safe=False)


def resumen(request):
    datos = []
    for institucion in Institucion.objects.all():
        dato = {'nombre': institucion.nombre or institucion.datos.get("codigo")}
        for anio in [2015, 2016, 2017, 2018, 2019, 2020]:
            respuestas = Respuesta.objects.filter(anio=anio, institucion=institucion)
            if respuestas.count() == 0:
                continue

            dato[anio] = get_valores(respuestas, 'eval_inst')["neta"]
        datos.append(dato)

    return JsonResponse(datos, safe=False)


def get_valores(respuestas, medicion):
    negativo_suma = respuestas.filter(**{'{}__in'.format(medicion): [1, 2, 3, 4]}).aggregate(suma=Sum('f_pond'))["suma"] or 0
    positivo_suma = respuestas.filter(**{'{}__in'.format(medicion): [6, 7]}).aggregate(suma=Sum('f_pond'))["suma"] or 0
    neutro_suma = respuestas.filter(**{'{}__in'.format(medicion): [5]}).aggregate(suma=Sum('f_pond'))["suma"] or 0
    suma = respuestas.filter(**{'{}__in'.format(medicion): [1, 2, 3, 4, 5, 6, 7]}).aggregate(suma=Sum('f_pond'))["suma"] or 0

    if suma is not None and suma > 0:
        positivo = round((positivo_suma) / suma * 100, 0)
        negativo = round((negativo_suma) / suma * 100, 0)
        neutro = round((neutro_suma) / suma * 100, 0)
    else:
        positivo = 0
        negativo = 0
        neutro = 0

    neta = positivo - negativo
    return {
        'negativo_suma': negativo_suma,
        'negativo_suma': negativo_suma,
        'neutro_suma': neutro_suma,
        'suma': suma,
        'neta': neta,
        'positivo': positivo,
        'negativo': negativo,
        'neutro': neutro,

    }
