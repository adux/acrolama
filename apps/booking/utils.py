import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlencode
from django.urls import reverse

from django.template.loader import render_to_string

from pprint import pprint

from project.models import Event, PriceOption, TimeOption, Irregularity
from users.models import User


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


def email_sender(instance, flag):
    """
    Signals could give Error cause you can call them from wherever.
    Save slows down.
    On the view in can be cached. an extra query is needed tho unless I pass
    the form instance. Want to TEST.
    https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    Theres another Method with Multi wich helps for headers if needed
    """
    irregularities = Irregularity.objects.filter(
        event__slug=instance.event.slug
    )
    # TODO: could come from config.
    sender = "notmonkeys@acrolama.com"
    to = ["acrolama@acrolama.com"]

    if flag == "Informed":
        subject = "Acrolama - Confirmation - " + str(instance.event)
        to += [instance.user.email]

        p = {
            "event": instance.event.title,
            "user": instance.user,
            "price": instance.price,
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
