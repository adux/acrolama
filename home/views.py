from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.utils import timezone
from datetime import datetime
from .models import(
    AboutMember,
    AboutGeneral,
    AboutDate,
    Event,
    Testimonial,
)

# Create your views here.i

def homeview(request):
    template_name='home.html'
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = AboutGeneral.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(datestart__gte=datetime.now()).order_by('datestart')[:5]
    qs_testimonial  = Testimonial.objects.all()
    context= {
        "about_content":qs_aboutmember,
        "about_general":qs_aboutgeneral,
        "about_date":qs_aboutdate,
        "event":qs_event,
        "testimonial":qs_testimonial,
    }
    return render(request, template_name, context)

class EventDetailView(DetailView):
    queryset = Event.objects.all()
