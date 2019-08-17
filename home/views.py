from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from home.multiforms import MultiFormsView
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
from project.models import Event, Location
from home.forms import NewsForm
from booking.forms import BookForm
from users.forms import UserRegisterForm, ProfileLoginForm
from home.filters import AccountingFilter, BookingFilter


@login_required(login_url="/error404/")
def accountingview(request):
    template_name = "accounting/accounting.html"
    acc_list = Accounting.objects.all()
    bk_list = Booking.objects.all()
    acc_filter = AccountingFilter(request.GET, queryset=acc_list)
    bk_filter = BookingFilter(request.GET, queryset=bk_list)
    context = {"filter_acc": acc_filter, "filter_bk": bk_filter}
    return render(request, template_name, context)


class HomeFormView(MultiFormsView):
    template_name = "home.html"
    form_classes = {
        "register": UserRegisterForm,
        "login": ProfileLoginForm,
        "news": NewsForm,
    }
    success_urls = {
        "register": reverse_lazy("home"),
        "login": reverse_lazy("home"),
        "news": reverse_lazy("home"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutMember.objects.all()
        context["about_general"] = About.objects.all()
        context["about_image"] = AboutImage.objects.all()
        context["about_date"] = AboutDate.objects.all()
        context["event"] = (
            Event.objects.filter(event_enddate__gte=timezone.now())
            .order_by("event_startdate", "title")
            .exclude(published=False)
            .exclude(category="fas fa-cogs")
            .distinct()[:6]
        )
        context["class"] = (
            Event.objects.filter(
                event_enddate__gte=timezone.now(), category="fas fa-cogs"
            )
            .order_by("event_startdate", "title")
            .exclude(published=False)
            .distinct()[:6]
        )
        context["testimonial"] = Testimonial.objects.all()
        context["portfolio"] = Portfolio.objects.order_by("order")[1:5]
        context["fportfolio"] = Portfolio.objects.order_by("order")[0:1]
        context["eporrfolio"] = Portfolio.objects.order_by("order")[5:6]
        return context

    def login_form_valid(self, form):
        form_name = form.cleaned_data.get("action")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self, username=username, password=password)
        if user is not None:
            login(self, user)
        return HttpResponseRedirect(self.get_success_url(form_name))

    def register_form_valid(self, form):
        instance = form.save(commit=False)
        form_name = form.cleaned_data.get("action")
        email = form.cleaned_data.get("email")
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Thanks. Please confirm your email: {email}",
        )
        instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))

    def news_form_valid(self, form):
        instance = form.save(commit=False)
        form_name = form.cleaned_data.get("action")
        email = form.cleaned_data.get("email")
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Thanks. Please confirm your email: {email}",
        )
        instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))


# faq.html
def faqview(request):
    qs_faq = Faq.objects.all()
    template_name = "faq.html"
    context = {"faq": qs_faq}
    return render(request, template_name, context)


# For the info pages
class InfoDetailView(DetailView):
    model = Info
    context_object_name = "info"


class EventListView(ListView):
    model = Event
    template_name = "home/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Event.objects.order_by("event_startdate")
            .exclude(category="fas fa-cogs")
            .exclude(published=False)
        )
        return context


class ClassListView(ListView):
    model = Event
    template_name = "home/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Event.objects.order_by("event_startdate")
            .filter(category="fas fa-cogs")
            .exclude(published=False)
        )
        return context
