from django.shortcuts import render
from django import forms
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from django.core.mail import send_mail
from django.db import connection

from project.models import Event, TimeOption, PriceOption, Exception
from booking.forms import BookForm
from users.models import User


class EventDisplay(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs
        context["form"] = BookForm(slug)
        context["timeoption"] = TimeOption.objects.filter(
            timelocation__event__slug=self.object.slug
        )
        context["priceoption"] = PriceOption.objects.filter(
            event__slug=self.object.slug
        )
        context["teacher"] = User.objects.filter(
            eventteacher__slug=self.object.slug
        )
        context["exception"] = Exception.objects.filter(
            event__slug=self.object.slug
        )
        return context


class EventInterest(SingleObjectMixin, FormView):
    template_name = "project/event_detail.html"
    form_class = BookForm
    model = Event

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user = request.user
        if form.is_valid():
            return self.form_valid(form, user)
        else:
            return self.form_invalid(form, user)

    def form_valid(self, form, user):
        instance = form.save(commit=False)
        instance.event = Event.objects.get(slug=self.object.slug)
        instance.user = user
        subject = "Acrolama - Confirmation - " + str(instance.event)
        message = (
            "Hoi "
            + instance.user.first_name
            + "\r\n\r\nThanks for registering for our Class: "
            + str(instance.event)
            + "!\r\n\r\nLamas are little rebels, unlike monkeys, we're bad at routine jobs. Fly dope tho...\r\n\r\nAnyway, in the next 72 hours you will receive an email concerning your registration status. In the meantime maybe take a look at our Instagram: https://instagram.com/acrolama or visit the FAQ if you have questions: https://acrolama.com/faq .\r\n\r\n\r\nHope to see you soon!\r\n\r\nBig Hug\r\nThe Lamas"
        )
        sender = "notmonkeys@acrolama.com"
        to = [instance.user.email, "acrolama@acrolama.com"]
        send_mail(subject, message, sender, to)
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home")


class EventDetail(View):
    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventInterest.as_view()
        return view(request, *args, **kwargs)
