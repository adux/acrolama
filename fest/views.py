from django.shortcuts import render
from .models import (
    Workshop,
)
# Create your views here.

def fest_homeview(request):
    template_name='index.html'
    qs  = Workshop.objects.all()
    context={
        }
    return render(request, template_name,context)
def fest_locationview(request):
    template_name='location.html'
    context={}
    return render(request, template_name,context)
def fest_pricesview(request):
    template_name='prices.html'
    context={}
    return render(request, template_name, context)
def fest_workshopsview(request):
    template_name='workshops.html'
    context={}
    return render(request, template_name, context)
