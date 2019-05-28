from datetime import datetime
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import (DetailView, CreateView, ListView)
from django.views.generic.edit import FormMixin
from home.models import (
    AboutMember,
    About,
    AboutImage,
    AboutDate,
    Accounting,
    Booking,
    Faq,
    FaqValues,
    Info,
    InfoImage,
    Testimonial,
    Portfolio,
)
from project.models import (
    Event,
    Location,
)
from home.forms import (
    NewsForm,
)
from booking.forms import (
    BookForm
)
from users.forms import (
    UserRegisterForm
)
from home.filters import (
    AccountingFilter,
    BookingFilter,
)

# Accounting con login requerido TODO: mejorar sistema de login a algo mas secreto ...
@login_required(login_url='/error404/')
def accountingview(request):
    template_name = 'accounting/accounting.html'
    acc_list = Accounting.objects.all()
    bk_list = Booking.objects.all()
    acc_filter = AccountingFilter(request.GET, queryset=acc_list)
    bk_filter = BookingFilter(request.GET, queryset=bk_list)
    context = {
        "filter_acc":acc_filter,
        "filter_bk":bk_filter,
    }
    return render(request, template_name, context)

def successview(request):
    template_name='success.html'
    return render(request, template_name)

# home de home.html
def homeview(request):
    template_name='home.html'
    form = UserRegisterForm( request.POST or None)
    errors = None
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = About.objects.all()
    qs_aboutimage   = AboutImage.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(event_enddate__gte=timezone.now()).order_by('event_startdate', 'title').exclude(published=False).exclude(category='fas fa-cogs').distinct()[:6]
    qs_class        = Event.objects.filter(event_enddate__gte=timezone.now(), category='fas fa-cogs').order_by('event_startdate', 'title').exclude(published=False).distinct()[:6]
    qs_testimonial  = Testimonial.objects.all()
    qs_portfolio    = Portfolio.objects.order_by('order')[1:5]
    qs_pfstart      = Portfolio.objects.order_by('order')[0:1]
    qs_pfend        = Portfolio.objects.order_by('order')[5:6]
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Thanks {username}. Please confirm your email.')
    if form.errors:
        errors = form.errors
    context= {
        "about_content":qs_aboutmember,
        "about_general":qs_aboutgeneral,
        "about_image":qs_aboutimage,
        "about_date":qs_aboutdate,
        "event":qs_event,
        "class":qs_class,
        "testimonial":qs_testimonial,
        "portfolio":qs_portfolio,
        "fportfolio":qs_pfstart,
        "eportfolio":qs_pfend,
        "form":form,
        "errors":errors,
    }
    return render(request, template_name, context)

# faq.html
def faqview(request):
    qs_faq = Faq.objects.all()
    template_name= 'faq.html'
    context = {
        "faq" : qs_faq
    }
    return render(request, template_name, context)


# For the info pages
class InfoDetailView(DetailView):
    model = Info
    context_object_name = 'info'


class EventListView(ListView):
    model = Event
    template_name = 'home/event_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Event.objects.order_by('event_startdate').exclude(category='fas fa-cogs').exclude(published=False)
        return context


class ClassListView(ListView):
    model = Event
    template_name = 'home/class_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Event.objects.order_by('event_startdate').filter(category='fas fa-cogs').exclude(published=False)
        return context
