import datetime

from allauth.account.models import EmailAddress

from dal import autocomplete
from django.db.models import Q  # Queries with OR
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from herdi.utils import (
    staff_check,
    herd_check,
)

from project.models import (
    Event,
    TimeOption,
    TimeLocation,
    Irregularity,
    PriceOption,
)
from audiovisual.models import Image, Video
from users.models import User
from booking.models import Book

from herdi.forms import InvitationForm
from invitations.utils import get_invitation_model

from booking.filters import BookFilter

# Create your views here.


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "herdi/herd.html"
    login_url = "/accounts/login/"

    def test_func(self):
        return herd_check(self.request.user)


@login_required
@user_passes_test(herd_check)
def invitationsendview(request):
    template = "herdi/invitation_create.html"
    form = InvitationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            Invitation = get_invitation_model()
            email = form.cleaned_data["email"]
            invite = Invitation.create(email, inviter=request.user)
            try:
                invite.send_invitation(request)
            except Exception as e:
                messages.add_message(request, messages.INFO, _("Error: " + e))
            else:
                messages.add_message(request, messages.INFO, _("Email sent to: " + email + " . We'll be in touch!"))
            return redirect("teacher_attendance")

    context = {
        "form": form,
    }
    return render(request, template, context)


@login_required
@user_passes_test(staff_check)
def contactlistview(request):
    template = "herdi/contact_list.html"
    booking_filter = BookFilter(
        request.GET,
        queryset=(
            Book.objects.all().select_related("event", "user", "price", "bookuserinfo")
            .prefetch_related("times")
            .order_by("-booked_at")
        ),
    )

    # Pagination
    paginator = Paginator(booking_filter.qs, 34)  # Show 24 contacts per page.
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "book_filter": booking_filter,
        "filter": request.GET,
        "page_obj": response,
    }

    return render(request, template, context)


class EventAutocomplete(autocomplete.Select2QuerySetView):
    """
    Get all the Events from the past year ordered by startdate and level
    """

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Event.objects.none()

        qs = (
            Event.objects.all()
            .filter(event_enddate__gte=datetime.datetime.now() - datetime.timedelta(days=356))
            .order_by("-event_startdate", "level")
            .select_related("project", "level")
        )

        if self.q:
            qs = qs.filter(
                Q(category__icontains=self.q)
                | Q(level__name__icontains=self.q)
                | Q(title__icontains=self.q)
            )

        return qs


class EventTeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Event.objects.none()

        qs = (
            Event.objects.all()
            .order_by("-event_startdate")
            .select_related("project", "level")
            .filter(teachers=self.request.user)
        )

        if self.q:
            qs = qs.filter(
                Q(category__icontains=self.q)
                | Q(level__name__icontains=self.q)
                | Q(title__icontains=self.q)
            )

        return qs


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return User.objects.none()

        none_verified = EmailAddress.objects.filter(verified=False).values_list('user_id', flat=True)
        qs = User.objects.exclude(pk__in=none_verified).order_by("last_name")

        if self.q:
            qs = qs.filter(
                Q(email__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )

        return qs


class TeachersAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return User.objects.none()

        qs = cache.get_or_set(
            "cache_teachers_all",
            User.objects.all().order_by("last_name").filter(is_teacher=True),
            120,
        )

        if self.q:
            qs = qs.filter(
                Q(email__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
            )

        return qs


class TimeOptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return TimeOption.objects.none()

        qs = TimeOption.objects.all().order_by("name")

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q)
                | Q(regular_day__icontains=self.q)
            )

        return qs


class TimeLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return TimeLocation.objects.none()

        # qs = TimeLocation.objects.all().order_by("name", "location").select_related("location")
        qs = cache.get_or_set(
            "cache_time_locations", TimeLocation.objects.all(), 120
        )

        if self.q:
            qs = qs.filter(
                Q(location__name__icontains=self.q)
                | Q(time_option__name__icontains=self.q)
                | Q(name__icontains=self.q)
            )

        return qs


class IrregularityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Irregularity.objects.none()

        qs = cache.get_or_set(
            "cache_irregularities_all",
            Irregularity.objects.all().order_by("-id"),
            120,
        )

        if self.q:
            qs = qs.filter(
                Q(time_location__name__icontains=self.q)
                | Q(description__icontains=self.q)
            )

        return qs


class PriceOptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return PriceOption.objects.none()

        qs = cache.get_or_set(
            "cache_price_options_all", PriceOption.objects.all(), 120
        )

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q)
                | Q(price_chf__icontains=self.q)
                | Q(name__icontains=self.q)
            )

        return qs


class ImagesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return Image.objects.none()

        # qs = PriceOption.objects.all().order_by("name")
        qs = cache.get_or_set("cache_image_all", Image.objects.all(), 120)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs


class VideosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return Video.objects.none()

        # qs = PriceOption.objects.all().order_by("name")
        qs = cache.get_or_set("cache_video_all", Video.objects.all(), 120)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs
