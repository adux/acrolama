import datetime
import accounting.utils

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save


INVOICESTATUS = [
    ("PE", "Pending"),
    ("PY", "Paid"),
    ("CA", "Canceled"),
    ("ST", "Storno"),
    ("FR", "First Reminder"),
    ("SR", "Second Reminder"),
    ("TR", "Third Reminder"),
]

BALANCE = [
    ("DB", "DEBIT"),
    ("CR", "CREDIT")
]

METHODE = [
    ("BT", "Bank"),
    ("TW", "Twint"),
    ("PP", "PayPal"),
    ("CS", "Cash"),
    ("CR", "Credit Card"),
    ("UN", "Unclasified"),
    ("RC", "Recovery Card"),
]


class Partner(models.Model):
    """
    TODO: Create a partener for every teacher on signal
    """
    name = models.CharField(max_length=50)
    address = models.ForeignKey("address.Address", null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    iban = models.CharField(max_length=50, null=True, blank=True)
    swift = models.CharField(max_length=50, null=True, blank=True)
    prefered_pay = models.CharField(max_length=15, choices=METHODE, null=True, blank=True)
    notes = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    balance = models.CharField(max_length=11, choices=BALANCE)
    book = models.OneToOneField("booking.Book", null=True, blank=True, on_delete=models.CASCADE)
    partner = models.ForeignKey("accounting.Partner", on_delete=models.CASCADE, null=True, blank=True)
    referral_code = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=INVOICESTATUS, default="PE")
    to_pay = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pay_till = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    pay_date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    reminder_dates = ArrayField(models.DateField(), size=3, null=True, blank=True)
    methode = models.CharField(max_length=15, choices=METHODE, default="UN", null=True, blank=True)
    notes = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.book:
            return "%s - %s" % (self.id, self.book)
        else:
            return "%s - %s" % (self.id, self.partner)

    def clean(self, *args, **kwargs):
        """
        Some crusal cleaning of the database to keep it consistent and clean with rather expected behaviours
        """

        if (self.paid and not self.pay_date) or (self.pay_date and not self.paid):
            raise ValidationError(_("Can't save. Paid invoices need a date and payment of min. 0."))

        if self.status in ("PY", "ST"):
            if not self.methode or (self.methode == "UN"):
                raise ValidationError(_("Can't save. Paid invoices need a payment methode."))
            if not self.paid or not self.pay_date:
                raise ValidationError(_("Can't save. Paid invoices need a date and payment of min. 0."))

        if (self.status in ("PE", "CA", "FR", "SR", "TR")) and (self.pay_date):
            raise ValidationError(_("Can't save. Is it paid? Valid status: Paid, Storno."))

        if self.reminder_dates and len(self.reminder_dates) > 1:
            if self.reminder_dates[-2] + datetime.timedelta(2) > self.reminder_dates[-1]:
                raise ValidationError(_("Can't save. Reminders need to be send 2 days apart min."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Invoice, self).save(*args, **kwargs)


def invoice_pre_save_referenz(sender, instance, *args, **kwargs):
    if not instance.pk:
        referenzstr = '{}00{}'.format(instance.book.user.pk, instance.book.pk)
        instance.referral_code = accounting.utils.finalize_referenz(referenzstr)


pre_save.connect(invoice_pre_save_referenz, sender=Invoice)
