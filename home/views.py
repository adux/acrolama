from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from datetime import datetime

from .models import(
    AboutMember,
    AboutGeneral,
    AboutDate,
    Event,

)

# Create your views here.i

def homeview(request):
    template_name='home.html'
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = AboutGeneral.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(datestart_event__gte=datetime.now()).order_by('datestart_event')[:5]
    context= {
        "about_content":qs_aboutmember,
        "about_general":qs_aboutgeneral,
        "about_date":qs_aboutdate,
        "event":qs_event,
    }
    return render(request, template_name, context)

class EventView(TemplateView):
    template_name='event.html'

