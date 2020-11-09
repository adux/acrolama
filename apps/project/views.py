from collections import defaultdict

from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

# Utils
from booking.utils import (
    email_sender,
    build_url,
    staff_check,
)

# from booking.services import (
#     inform_book,
# )

# Models
from project.models import Event, TimeOption, PriceOption, Irregularity, TimeLocation
from users.models import User

# Forms
from project.forms import EventUpdateForm, EventMinimalCreateForm
from booking.forms import BookForm, BookDuoInfoForm, BookDateInfoForm

# Filters
from project.filters import EventFilter


# EvenDetail for Explain
class EventDisplay(DetailView):
    """ "
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
                conditional["formduo"].append(obj.id)
            elif obj.single_date:
                conditional["formdate"].append(obj.id)
        return conditional

    def get_fromatedtimelocations(self, timelocations):
        formatedtimelocations = []
        key = ["location", "regular_day", "open_starttime", "open_endtime", "class_starttime", "class_endtime"]
        for obj in timelocations:
            location = [obj.location]
            time_options = obj.time_options.all()
            for to in time_options:
                timelocation = location + [
                    to.get_regular_day_display(),
                    to.open_starttime,
                    to.open_endtime,
                    to.class_starttime,
                    to.class_endtime,
                ]
            formatedtimelocations.append(dict(zip(key, timelocation)))
        return formatedtimelocations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Queries
        exceptions = Irregularity.objects.filter(event__slug=self.object.slug)
        teachers = User.objects.filter(eventteacher__slug=self.object.slug)
        prices = PriceOption.objects.filter(event__slug=self.object.slug)
        timelocations = TimeLocation.objects.filter(event__slug=self.object.slug)
        timeoptions = TimeOption.objects.filter(timelocation__event__slug=self.object.slug)

        # Extra Formats
        conditional = self.get_formconditional(prices)
        timelocations = self.get_fromatedtimelocations(timelocations)

        # Forms
        form = BookForm(prefix="booking")
        form.fields["price"].queryset = prices
        form.fields["times"].queryset = timeoptions
        formduo = BookDuoInfoForm(prefix="duo")
        formdate = BookDateInfoForm(prefix="date")

        # Context
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
        form = BookForm(self.request.POST, prefix="booking")
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        previous_url = self.get_object().get_absolute_url()
        messages.add_message(self.request, messages.ERROR, "Booking failed: Did you fill all the fields?")
        return HttpResponseRedirect(previous_url)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.event = self.get_object()
        instance.user = self.request.user

        prices = instance.event.price_options.all()
        conditionals = EventDisplay.get_formconditional(self, prices)

        if instance.price.id in conditionals["formduo"]:
            formduo = BookDuoInfoForm(self.request.POST, prefix="duo")
            if formduo.is_valid():
                instance_duo = formduo.save(commit=False)
                instance.save()
                form.save_m2m()
                instance_duo.book = instance
                instance_duo.save()

        if instance.price.id in conditionals["formdate"]:
            formdate = BookDateInfoForm(self.request.POST, prefix="date")
            if formdate.is_valid():
                instance_date = formdate.save(commit=False)
                instance.save()
                form.save_m2m()
                instance_date.book = instance
                instance_date.save()

        instance.save()
        form.save_m2m()

        # save all m2m of instance
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


@login_required
@user_passes_test(staff_check)
def eventlistview(request):
    template = "project/event_list.html"

    event_filter = EventFilter(
        request.GET,
        queryset=(
            Event.objects.all()
            # .select_related("project", "policy", "level", "discipline")
            .select_related(
                "project",
                "level",
            ).order_by("-event_startdate")
        ),
    )

    if request.method == "POST":
        if "newevent" in request.POST:
            form = EventMinimalCreateForm(request.POST)
            if form.is_valid():
                event = form.save()
                return redirect("event_update", event.pk)
    else:
        form = EventMinimalCreateForm()

    # Pagination
    paginator = Paginator(event_filter.qs, 24)  # Show 24 contacts per page.
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "event_filter": event_filter,
        "filter": request.GET,
        "form": form,
        "page_obj": response,
    }

    return render(request, template, context)


# class EventUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
#     model = Event
#     template_name = "project/event_update.html"
#     form_class = EventUpdateForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         event_filter = EventFilter(
#             self.request.GET,
#             queryset=(
#                 Event.objects.all()
#                 .select_related("project", "level")
#             )
#         )

#         # Paginator
#         paginator = Paginator(event_filter.qs, 24)  # Show 24 contacts per page.
#         page = self.request.GET.get("page")
#         try:
#             response = paginator.page(page)
#         except PageNotAnInteger:
#             response = paginator.page(1)
#         except EmptyPage:
#             response = paginator.page(paginator.num_pages)

#         # Context
#         context["page_obj"] = response
#         context["filter"] = self.request.GET
#         context["event_filter"] = event_filter

#         return context

#     def get_success_url(self, **kwargs):
#         url = build_url(
#             "event_list",
#             get=self.request.GET.items(),
#         )
#         return url

#     def test_func(self):
#         return staff_check(self.request.user)


@login_required
@user_passes_test(staff_check)
def EventUpdateView(request, pk):
    template = "project/event_update.html"

    obj = cache.get_or_set("cache_event_" + str(pk), get_object_or_404(Event, id=pk), 120)

    def cache_m2m(fields=[], obj=None):
        cached_m2m = {}
        for f in fields:
            cached_obj = cache.get_or_set(
                "cached_" + f + "_event" + str(obj.id), [p.id for p in getattr(obj, str(f)).all()], 120
            )
            cached_m2m.update({str(f): cached_obj})
        return cached_m2m

    initial = cache_m2m(["time_locations", "price_options", "teachers", "irregularities", "images", "videos"], obj)

    initial.update(
        {
            # fk
            "project": obj.project.id,
            "policy": obj.policy.id,
            "level": obj.level.id,
            "discipline": obj.discipline.id,
            # fields
            "category": obj.category,
            "cycle": obj.cycle,
            "title": obj.title,
            "event_startdate": obj.event_startdate,
            "event_enddate": obj.event_enddate,
            "description": obj.description,
            "max_participants": obj.max_participants,
            "prerequisites": obj.prerequisites,
            "highlights": obj.highlights,
            "included": obj.included,
            "food": obj.food,
            "published": obj.published,
            "registration": obj.registration,
        }
    )

    if request.method == "POST":
        form = EventUpdateForm(request.POST, instance=obj,)

        if form.is_valid():
            form.save()

    else:
        form = EventUpdateForm(initial=initial, instance=obj)

    context = {
        "filter": request.GET,
        "form": form,
    }

    return render(request, template, context)
