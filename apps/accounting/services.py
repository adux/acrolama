import datetime

# Send email with template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from accounting.models import Invoice


def invoice_get(invoice):
    if isinstance(invoice, (str, int)):
        invoice_pk = int(invoice)
    else:
        return invoice

    if invoice_pk:
        try:
            invoice = Invoice.objects.get(pk=invoice_pk)
        except Exception:
            return

    return invoice


def invoice_reminder(instance, invoice):
    # Send the Informed Email and add the date
    if instance.status == "FR":
        if not invoice.reminder_dates:
            invoice_send_reminder(instance)
            instance.reminder_dates = [datetime.datetime.now().date()]
        else:
            raise Exception(_("First reminder error, already sent? " + str(invoice.reminder_dates[-1])))

    if instance.status == "SR":
        if len(invoice.reminder_dates) == 1:
            invoice_send_reminder(instance)
            instance.reminder_dates.append(datetime.datetime.now().date())
        else:
            raise Exception(_("Second reminder error, already sent? " + str(invoice.reminder_dates[-1])))

    if instance.status == "TR":
        if len(invoice.reminder_dates) == 2:
            invoice_send_reminder(instance)
            instance.reminder_dates.append(datetime.datetime.now().date())
        else:
            raise Exception(_("Third reminder error, already sent? " + str(invoice.reminder_dates[-1])))


def invoice_send_reminder(invoice):
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]
    subject = "Acrolama - Payment Reminder - " + str(invoice.book.event.title)
    to = [invoice.book.user.email]

    context = {
        "invoice": invoice,
        "user": invoice.book.user,
        "event": invoice.book.event,
    }

    msg_plain = render_to_string(
        settings.BASE_DIR + "/apps/accounting/templates/accounting/email_reminder.txt",
        context,
    )
    msg_html = render_to_string(
        settings.BASE_DIR + "/apps/accounting/templates/accounting/email_reminder.html",
        context,
    )

    msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()


def invoice_send_paid(invoice):
    sender = "notmonkeys@acrolama.com"
    bcc = ["acrolama@acrolama.com"]
    subject = "Acrolama - Payment Confirmation -  " + str(invoice.book.event.title)
    to = [invoice.book.user.email]

    context = {
        "event": invoice.book.event,
        "user": invoice.book.user,
        "price": invoice.book.price,
        "times": invoice.book.times.all,
    }

    msg_plain = render_to_string(
        settings.BASE_DIR + "/apps/accounting/templates/accounting/email_paid.txt",
        context,
    )
    msg_html = render_to_string(
        settings.BASE_DIR + "/apps/accounting/templates/accounting/email_paid.html",
        context,
    )
    msg = EmailMultiAlternatives(subject, msg_plain, sender, to, bcc)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
