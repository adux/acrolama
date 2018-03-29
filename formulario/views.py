from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import(
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from formulario.forms import FestForm
from formulario.models import Fest

# Create your views here.

def festprueba_createview(request):
    if request.method == "POST":
        form = FestForm(request.POST)
        if form.is_valid():
            obj = fest.objects.create(
                   name         = form.cleaned_data.get('name'),
                   address      = form.cleaned_data.get('address'),
                   numero       = form.cleaned_data.get('numero'),
                   email        = form.cleaned_data.get('email'),
                   option       = form.cleaned_data.get('option'),
                   allergies    = form.cleaned_data.get('allergies')
                )
        if form.errors:
            print(form.errors)
    template_name='form.html'
    context={}
    return render (request, template_name, context)

def fest_createview(request):
    if request.method == "POST":
        print("post data")
        form = FestForm(request.POST)
        if form.is_valid():
            obj = Fest.objects.create(
                   name         = form.cleaned_data.get('name'),
                   address      = form.cleaned_data.get('address'),
                   numero       = form.cleaned_data.get('numero'),
                   email        = form.cleaned_data.get('email'),
                   option       = form.cleaned_data.get('option'),
                   allergies    = form.cleaned_data.get('allergies')
                )
        if form.errors:
            print(form.errors)
    template_name='homeform.html'
    context={}
    return render (request, template_name, context)
