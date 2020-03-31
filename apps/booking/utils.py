import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlencode
from django.urls import reverse

from django.template.loader import render_to_string

from project.models import Event, PriceOption, TimeOption, Irregularity
from accounting.models import Invoice

# from users.models import User

# Tests for the UserPassesTestMixin
def staff_check(user):
    return user.is_staff

def teacher_check(user):
    return user.is_teacher

def herd_check(user):
    if user.is_teacher or user.is_staff:
        return True
    else:
        return False


#  TODO: im not sure what kwargs.pop does. or if i can handle it differently
def build_url(*args, **kwargs):
    get = kwargs.pop("get", {})
    pk = kwargs.pop("pk", {})
    # TODO: this kwargs=pk doesn't look good, works, but i think its
    # super unelegant
    url = reverse(*args, kwargs=pk)
    if get:
        url += "?" + urlencode(get)
    return url


def datelistgenerator(startdate, enddate, regularday):
    dateList = []
    delta = enddate - startdate + datetime.timedelta(days=1)

    for x in range(delta.days):
        checkdate = startdate + datetime.timedelta(days=x)
        if checkdate.weekday() == regularday:
            dateList.append(checkdate)

    return dateList


def space_out(string, length):
    return ' '.join(string[i:i+length] for i in range(0,len(string),length))


def email_sender(instance, flag):
    """
    Signals could give Error cause you can call them from wherever.
    Save slows down.
    On the view in can be cached. an extra query is needed tho unless I pass
    the form instance. Want to TEST.
    https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    Theres another Method with Multi wich helps for headers if needed
    """
    # TODO: could come from config.
    sender = "notmonkeys@acrolama.com"
    to = ["acrolama@acrolama.com"]

    if flag == "Informed":
        subject = "Acrolama - Confirmation - " + str(instance.event.title)
        to += [instance.user.email]

        irregularities = Irregularity.objects.filter(
            event__slug=instance.event.slug
        )

        #TODO: Unnecesary access to DB
        invoice = Invoice.objects.get(book=instance.pk)
        referenznum = space_out(
            str(instance.user.pk)
            + "00"
            + str(instance.event.pk)
            + "00"
            + str(instance.pk)
            + "00"
            + str(invoice.pk)
            ,4
        )

        p = {
            "event": instance.event,
            "user": instance.user,
            "price": instance.price,
            "referenznum": referenznum,
            "pay_till": invoice.pay_till,
            "times": instance.times.all,
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_informed.txt",
            p,
        )
        msg_html = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_informed.html",
            p,
        )

        send_mail(subject, msg_plain, sender, to, html_message=msg_html)

    elif flag == "Paid":
        subject = "Acrolama - Payment Confirmation - " + str(
            instance.book.event.title
        )
        to += [instance.book.user.email]

        irregularities = Irregularity.objects.filter(
            event__slug=instance.book.event.slug
        )

        p = {
            "event": instance.book.event,
            "user": instance.book.user,
            "price": instance.book.price,
            "times": instance.book.times.all,
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_paid.txt",
            p,
        )
        msg_html = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_paid.html",
            p,
        )
        send_mail(subject, msg_plain, sender, to, html_message=msg_html)

    elif flag == "Registered":
        subject = "Acrolama - Registration - " + str(instance.event.title)
        sender = "notmonkeys@acrolama.com"
        to += [instance.user.email]

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
