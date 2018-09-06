from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
)
from django.views.generic.edit import FormMixin
from home.models import (
    AboutMember,
    About,
    AboutImage,
    AboutDate,
    Accounting,
    Booking,
    Event,
    Info,
    InfoImage,
    Testimonial,
    Portfolio,
)
from home.forms import (
    PortfolioCreateForm,
    BookClassCreateForm,
    BookEventCreateForm,
    NewsForm,
)
from home.filters import (
    AccountingFilter,
    BookingFilter,
)
@login_required(login_url='/error404/')
def accountingview(request):
    acc_list = Accounting.objects.all()
    bk_list = Booking.objects.all()
    acc_filter = AccountingFilter(request.GET, queryset=acc_list)
    bk_filter = BookingFilter(request.GET, queryset=bk_list)
    context = {
        "filter":acc_filter,
        "filter_bk":bk_filter,
    }
    return render(request, 'accounting.html', context)

def homeview(request):
    template_name='home.html'
    form = NewsForm( request.POST or None)
    errors = None
    qs_aboutmember  = AboutMember.objects.all()
    qs_aboutgeneral = About.objects.all()
    qs_aboutimage   = AboutImage.objects.all()
    qs_aboutdate    = AboutDate.objects.all()
    qs_event        = Event.objects.filter(dateend__gte=timezone.now()).order_by('datestart').exclude(cat='fas fa-cogs').exclude(published=False)[:5]
    qs_class        = Event.objects.filter(dateend__gte=timezone.now()).order_by('datestart').filter(cat='fas fa-cogs').exclude(published=False)[:5]
    qs_testimonial  = Testimonial.objects.all()
    qs_portfolio    = Portfolio.objects.order_by('order')[1:5]
    qs_pfstart      = Portfolio.objects.order_by('order')[0:1]
    qs_pfend        = Portfolio.objects.order_by('order')[5:6]
    if form.is_valid():
        form.save()
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


class InfoDetailView(DetailView):
    model = Info
    context_object_name = 'info'


class EventListView(ListView):
    model = Event
    template_name = 'home/event_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Event.objects.order_by('datestart').exclude(cat='fas fa-cogs').exclude(published=False)
        return context


class ClassListView(ListView):
    model = Event
    template_name = 'home/class_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Event.objects.order_by('datestart').filter(cat='fas fa-cogs').exclude(published=False)
        return context


class ClassDetailView(FormMixin, DetailView):
    model = Event
    form_class = BookClassCreateForm
    template_name = 'home/class_detail.html'
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Thanks for Registering! See you soon!')
        return reverse('classes',kwargs={'slug':self.object.slug})
    def get_context_data(self,**kwargs):
        context = super(ClassDetailView,self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.event = Event.objects.get(slug = self.object.slug)
        instance.option = instance.event.get_ocurrance_display()
        instance.save()
        return super(ClassDetailView, self).form_valid(form)


class EventDetailView(FormMixin, DetailView):
    model = Event
    form_class = BookEventCreateForm
    template_name = 'home/event_detail.html'
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Thanks for Registering! See you soon!')
        return reverse('events',kwargs={'slug':self.object.slug})
    def get_context_data(self,**kwargs):
        context = super(EventDetailView,self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.event = Event.objects.get(slug = self.object.slug)
        instance.save()
        return super(EventDetailView, self).form_valid(form)


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
