from django.conf import settings

from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages

from project.models import Event, TimeOption, PriceOption, Irregularity
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
        context["exception"] = Irregularity.objects.filter(
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
        # TODO: I think there are some optimisations to be done here. Args
        # don't seem to right.
        instance = form.save(commit=False)
        instance.event = Event.objects.get(slug=self.object.slug)
        # TODO: can't i just use self.request.user ? TEST
        instance.user = user
        subject = "Acrolama - Registration - " + str(instance.event)
        sender = "notmonkeys@acrolama.com"
        to = [instance.user.email, "acrolama@acrolama.com"]
        p = {
            "event": instance.event,
            "user": instance.user,
        }

        msg_plain = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_registration.txt",
            p,
        )
        msg_html = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_registration.html",
            p,
        )
        send_mail(subject, msg_plain, sender, to, html_message=msg_html)
        instance.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Thank you for registering')
        return self.request.path


class EventDetail(View):
    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventInterest.as_view()
        return view(request, *args, **kwargs)
