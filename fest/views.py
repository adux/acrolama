from django.shortcuts import render
from .models import (
    Workshop,
)


def fest_homeview(request):
    template_name = 'index.html'
    context = {}
    return render(request, template_name, context)


def fest_locationview(request):
    template_name = 'location.html'
    context = {}
    return render(request, template_name, context)


def fest_pricesview(request):
    template_name = 'prices.html'
    context = {}
    return render(request, template_name, context)


def fest_workshopsview(request):
    template_name = 'workshops.html'
    qs_jueves = Workshop.objects.filter(date='2018-03-08').order_by('time')
    qs_viernes = Workshop.objects.filter(date='2018-03-09').order_by('time')
    qs_sabado = Workshop.objects.filter(date='2018-03-10').order_by('time')
    qs_domingo = Workshop.objects.filter(date='2018-03-11').order_by('time')
    context = {
        "jueves": qs_jueves,
        "viernes": qs_viernes,
        "sabado": qs_sabado,
        "domingo": qs_domingo
    }
    return render(request, template_name, context)


def frontpage_view(request):
    template_name = 'pages/frontpage.html'
    context = {}
    return render(request, template_name, context)
