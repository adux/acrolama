from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
)

from home.models import (
    AboutMember,
    AboutGeneral,
    AboutDate,
    Event,
    Testimonial,
    Portfolio,
)
from home.forms import (
    PortfolioCreateForm,
)

def homeview(request):
    template_name='home.html'
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = AboutGeneral.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(datestart__gte=datetime.now()).order_by('datestart')[:5]
    qs_testimonial  = Testimonial.objects.all()
    qs_portfolio    = Portfolio.objects.order_by('uploaded_at')[1:5]
    qs_pfstart      = Portfolio.objects.order_by('uploaded_at')[0:1]
    qs_pfend        = Portfolio.objects.order_by('uploaded_at')[5:6]
    positions       = ['p_one','p_one_half',]
    context= {
        "about_content":qs_aboutmember,
        "about_general":qs_aboutgeneral,
        "about_date":qs_aboutdate,
        "event":qs_event,
        "testimonial":qs_testimonial,
        "portfolio":qs_portfolio,
        "positions":positions,
        "fportfolio":qs_pfstart,
    }
    return render(request, template_name, context)

class EventDetailView(DetailView):
    queryset = Event.objects.all()

class PortfolioCreateView(LoginRequiredMixin, CreateView):
    form_class = PortfolioCreateForm
    template_name = 'home/portfolio_form.html'
    success_url = reverse_lazy('home/portfolio_form.html')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolios  = Portfolio.objects.all()
        context['portfolios'] = portfolios
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        #instance.save is done by CreateView
        return super(PortfolioCreateView, self).form_valid(form)

