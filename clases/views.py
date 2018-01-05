from django.http import HttpResponse
from django.shortcuts import render
#for class based view
from django.views import View
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name ='home.html'
