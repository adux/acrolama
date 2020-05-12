from collections import defaultdict

from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from django.contrib import messages

#Utils
from booking.utils import email_sender

#Models
from project.models import (
    Event,
    TimeOption,
    PriceOption,
    Irregularity,
    TimeLocation
)
from users.models import User

#Forms
from booking.forms import BookForm, BookDuoInfoForm, BookDateInfoForm

# EvenDetail for Explain
class EventDisplay(DetailView):
    """"
        Handels how the Form is going to look like in the First paint
        main_tl_list
        # Creates a list of lists:
        # (('location','regular_day','open_time...),('regu..)..)

        gets template from DetailView model_detail.html
        you could repain
    """
    model = Event

    def get_formconditional(self, prices):
        conditional = defaultdict(list)
        for obj in prices:
            if obj.duo:
                conditional['formduo'].append(obj.id)
            elif obj.single_date:
                conditional['formdate'].append(obj.id)
        return conditional

    def get_fromatedtimelocations(self, timelocations):
        formatedtimelocations = []
        key = ['location', 'regular_days', 'open_starttime', 'open_endtime', 'class_starttime', 'class_endtime']
        for obj in timelocations:
            location = [obj.location]
            time_options = obj.time_options.all()
            for to in time_options:
                timelocation = location + [to.regular_days,
                            to.open_starttime,
                            to.open_endtime,
                            to.class_starttime,
                            to.class_endtime
                            ]
            formatedtimelocations.append(dict(zip(key, timelocation)))
        return formatedtimelocations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Queries
        exceptions = Irregularity.objects.filter(event__slug=self.object.slug)
        teachers = User.objects.filter(eventteacher__slug=self.object.slug)
        prices = PriceOption.objects.filter(event__slug=self.object.slug)
        timelocations = TimeLocation.objects.filter(event__slug=self.object.slug)
        timeoptions = TimeOption.objects.filter(timelocation__event__slug=self.object.slug)

        # Extra Formats
        conditional = self.get_formconditional(prices)
        timelocations = self.get_fromatedtimelocations(timelocations)

        #Forms
        form = BookForm(prefix='booking')
        form.fields["price"].queryset = prices
        form.fields["times"].queryset = timeoptions
        formduo = BookDuoInfoForm(prefix='duo')
        formdate = BookDateInfoForm(prefix='date')

        #Context
        context["teachers"] = teachers
        context["exceptions"] = exceptions
        context["form"] = form
        context["formduo"] = formduo
        context["formdate"] = formdate
        context["conditional"] = conditional
        context["priceoptions"] = prices
        context["timelocations"] = timelocations
        return context


class EventInterest(SingleObjectMixin, FormView):
    """
    This ones writes the template again after the post
    """
    template_name = "project/event_detail.html"
    form_class = BookForm
    prefix = "booking"
    model = Event

    def post(self, request, *args, **kwargs):
        form = BookForm(self.request.POST, prefix='booking')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        previous_url = self.get_object().get_absolute_url()
        messages.add_message(
            self.request,
            messages.ERROR,
            'Booking failed: Did you fill all the fields?'
        )
        return HttpResponseRedirect(previous_url)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.event = self.get_object()
        instance.user = self.request.user

        prices = instance.event.price_options.all()
        conditionals = EventDisplay.get_formconditional(self, prices)

        if instance.price.id in conditionals["formduo"]:
            formduo = BookDuoInfoForm(self.request.POST, prefix='duo')
            if formduo.is_valid():
                instance_duo = formduo.save(commit=False)
                instance.save()
                form.save_m2m()
                instance_duo.book = instance
                instance_duo.save()
            else:
                return form_invalid(self, form)

        if instance.price.id in conditionals["formdate"]:
            formdate = BookDateInfoForm(self.request.POST, prefix='date')
            if formdate.is_valid():
                instance_date = formdate.save(commit=False)
                instance.save()
                form.save_m2m()
                instance_date.book = instance
                instance_date.save()
            else:
                return form_invalid(self, form)

        instance.save()
        form.save_m2m()

        #save all m2m of instance
        email_sender(instance, "Registered")
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Thank you for registering")
        return self.request.path


class EventDetail(View):
    """
    Passes the display in get and forms in the post
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview
    """
    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventInterest.as_view()
        return view(request, *args, **kwargs)
