from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    FormView,
)
from django.views.generic.detail import SingleObjectMixin

from home.models import (
    AboutMember,
    About,
    AboutImage,
    AboutDate,
    Booking,
    Event,
    Info,
    InfoImage,
    Testimonial,
    Portfolio,
)
from home.forms import (
    PortfolioCreateForm,
    BookingCreateForm,
)

def homeview(request):
    template_name='home.html'
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = About.objects.all()
    qs_aboutimage   = AboutImage.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(datestart__gte=datetime.now()).order_by('datestart')[:5]
    qs_testimonial  = Testimonial.objects.all()
    qs_portfolio    = Portfolio.objects.order_by('order')[1:5]
    qs_pfstart      = Portfolio.objects.order_by('order')[0:1]
    qs_pfend        = Portfolio.objects.order_by('order')[5:6]
    positions       = ['p_one','p_one_half',]
    context= {
        "about_content":qs_aboutmember,
        "about_general":qs_aboutgeneral,
        "about_image":qs_aboutimage,
        "about_date":qs_aboutdate,
        "event":qs_event,
        "testimonial":qs_testimonial,
        "portfolio":qs_portfolio,
        "positions":positions,
        "fportfolio":qs_pfstart,
        "eportfolio":qs_pfend,
    }
    return render(request, template_name, context)

class InfoDetailView(DetailView):
    model = Info
    context_object_name = 'info'

class Booking(SingleObjectMixin, FormView):
    template_name = 'home/event_detail.html'
    form_class = BookingCreateForm
    model = Booking
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(Booking, self).post(request, *args, **kwargs)
    def get_success_url(self):
        return reverse('home')

class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    def get_context_data(self,**kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context['form'] = BookingCreateForm(auto_id=False)
        return context

class EventView(View):
    def get(self,request,*args,**kwargs):
        view = EventDetailView.as_view()
        return view(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        view = Booking.as_view()
        return view(request,*args,**kwargs)


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

