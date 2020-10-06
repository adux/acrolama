import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlencode
from django.urls import reverse

from django.template.loader import render_to_string

from project.models import Irregularity

import booking.services


# Tests for the UserPassesTestMixin
def staff_check(user):
    return user.is_staff


def teacher_check(user):
    return user.is_teacher


def herd_check(user):
    try:
        if user.is_teacher or user.is_staff:
            return True
    except AttributeError:
        return False


def build_url(*args, **kwargs):
    get = kwargs.pop("get", {})
    pk = kwargs.pop("pk", {})
    # args has the url name for reverse
    # pk has to be an mapping
    url = reverse(*args, kwargs=pk)
    if get:
        url += "?" + urlencode(get)
    return url


def make_regularday_dates_list(startdate, enddate, regularday):
    dateList = []
    delta = enddate - startdate + datetime.timedelta(days=1)

    for x in range(delta.days):
        checkdate = startdate + datetime.timedelta(days=x)
        if checkdate.weekday() == regularday:
            dateList.append(checkdate)

    return dateList


def space_out(string, length):
    return " ".join(string[i: i + length] for i in range(0, len(string), length))


def email_sender(instance, flag):
    """
    Signals could give Error cause you can call them from wherever.
    Save slows down.
    https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    Theres another Method with Multi wich helps for headers if needed
    """
    # TODO: could come from config.
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]

    if flag == "Informed":
        subject = "Acrolama - Confirmation - " + str(instance.event.title)
        to = [instance.user.email]

        irregularities = Irregularity.objects.filter(event__slug=instance.event.slug)
        times = instance.times.all()
        location = booking.services.get_location_from_timeoption(times, instance.event)

        referenznum = space_out(
            str(instance.user.pk)
            + "0"
            + str(instance.event.pk)
            + "0"
            + str(instance.pk)
            + "0"
            + str(instance.invoice.pk),
            4,
        )

        p = {
            "event": instance.event,
            "user": instance.user,
            "price": instance.price,
            "referenznum": referenznum,
            "pay_till": instance.invoice.pay_till,
            "times": times,
            "location": location,
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_informed.txt", p,)
        msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_informed.html", p,)

        msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    elif flag == "Paid":
        subject = "Acrolama - Payment Confirmation -  " + str(instance.book.event.title)
        to = [instance.book.user.email]

        irregularities = Irregularity.objects.filter(event__slug=instance.book.event.slug)

        p = {
            "event": instance.book.event,
            "user": instance.book.user,
            "price": instance.book.price,
            "times": instance.book.times.all,
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_paid.txt", p,)
        msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_paid.html", p,)
        msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    elif flag == "Registered":
        subject = "Acrolama - Booking received - " + str(instance.event.title)
        sender = "notmonkeys@acrolama.com"
        to = [instance.user.email]

        p = {
            "event": instance.event,
            "user": instance.user,
        }

        msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_registration.txt", p,)
        msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_registration.html", p,)

        msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()

    elif flag == "Reminder":
        subject = "Acrolama - Reminder - " + str(instance.event.title)
        sender = "notmonkeys@acrolama.com"
        to = [instance.user.email]

        irregularities = Irregularity.objects.filter(event__slug=instance.event.slug)
        times = instance.times.all()
        location = booking.services.get_location_from_timeoption(times, instance.event)
        try:
            abocount = booking.services.get_count_abocounter_of_book(instance.id)
        except ObjectDoesNotExist:
            abocount = False

        p = {
            "event": instance.event,
            "user": instance.user,
            "times": times,
            "location": location,
            "abocount": abocount,
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_reminder.txt", p,)
        msg_html = render_to_string(settings.BASE_DIR + "/apps/booking/templates/booking/email_reminder.html", p,)

        msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
