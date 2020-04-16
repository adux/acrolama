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
from booking.forms import BookForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #kwargs is the object Event
        #self.kwargs contains the slug passed form the link
        #TODO: Still don't understand why i can't pass only the slug
        #ModelForm expects a dict so we pass the whole kwargs
        context["form"] = BookForm(self.kwargs)

        # Time Location list solution.
        # TODO: Make this a dictionary.
        #Maybe better way. Problem could be in
        # how models are allready done.
        # TODO: Im sure this is cachable for each event
        timelocations = TimeLocation.objects.filter(
            event__slug=self.object.slug
        )
        main_tl_list = []
        for timelocation in timelocations:
            tmp_list = []
            tmp_list.append(timelocation.location)
            timeoptions = timelocation.time_options.all()
            for timeoption in timeoptions:
                tmp_list.append(timeoption.regular_days)
                tmp_list.append(timeoption.open_starttime)
                tmp_list.append(timeoption.open_endtime)
                tmp_list.append(timeoption.class_starttime)
                tmp_list.append(timeoption.class_endtime)
            main_tl_list.append(tmp_list)

        context["timelocations_list"] = main_tl_list
        context["priceoptions"] = PriceOption.objects.filter(
            event__slug=self.object.slug
        )
        context["teachers"] = User.objects.filter(
            eventteacher__slug=self.object.slug
        )
        context["exceptions"] = Irregularity.objects.filter(
            event__slug=self.object.slug
        )
        #rest of the context as usual
        return context


class EventInterest(SingleObjectMixin, FormView):
    """
    This ones writes the template again after the post
    """
    template_name = "project/event_detail.html"
    form_class = BookForm
    model = Event

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        #Need to get user form request. self if Event Interest with obj Book
        if form.is_valid():
            #pass the user to the instance
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        #TODO: i would actually like to pass the form to EventDetail,
        #but passing context sucks speciall with all the slug workarround
        previous_url = self.request.POST.get('next', '/')
        messages.add_message(
            self.request,
            messages.WARNING,
            'Booking Failed: Did you select a Time Preference?'
        )
        return HttpResponseRedirect(previous_url)

    def form_valid(self, form):
        instance = form.save(commit=False)
        # Get the instance of the Model
        instance.event = self.get_object()
        instance.user = self.request.user
        instance.save()
        #save all m2m of instance
        form.save_m2m()
        email_sender(instance, "Registered")
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Thank you for registering")
        return self.request.path


class EventDetail(View):
    """
    Passes the display in get and forms in the post
    """
    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventInterest.as_view()
        return view(request, *args, **kwargs)
