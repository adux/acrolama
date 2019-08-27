from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from home.multiforms import MultiFormsView
from home.models import (
    AboutTeam,
    About,
    AboutImage,
    AboutDate,
    Faq,
    Info,
    Testimonial,
    Portfolio,
    Whatsapp,
)
from project.models import Event
from home.forms import NewsForm
from booking.forms import BookForm


class HomeFormView(MultiFormsView):
    template_name = "home.html"
    form_classes = {
        "news": NewsForm,
    }
    success_urls = {
        "news": reverse_lazy("home"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutTeam.objects.all()
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
        context["eportfolio"] = Portfolio.objects.order_by("order")[5:6]
        context["whatsapp"] = Whatsapp.objects.all()
        return context

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
