from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
# Create your views here.i

class HomeView(TemplateView):
    template_name='home.html'

class EventView(TemplateView):
    template_name='event.html'
