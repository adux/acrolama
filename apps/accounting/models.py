import datetime
import accounting.utils

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save


"""
status ->
    ("PE", "Pending") -> For Open not fully paid Credits
    ("PY", "Paid") -> for fully paid Credits
    ("CA", "Canceled") -> for over due unused credit
    ("ST", "Storno") -> doesn't applly
    ("FR", "First Reminder") -> Reminder of credit to be used
    ("SR", "Second Reminder") -> Reminder of credit can be used and canceled
    ("TR", "Third Reminder") -> Last reminder of Credit being canceled
to_pay -> total amount to be paid back by Acrolama
paid -> amount that has been paid till date
pay_till -> due of credit
pay_date -> dates of transactions
methode -> internal, credit or similar
notes -> some notes to the transaction
"""

INVOICESTATUS = [
    ("PE", "Pending"),
    ("PY", "Paid"),  # TODO: Change to PI
    ("CA", "Canceled"),
    ("ST", "Storno"),
    ("FR", "First Reminder"),
    ("SR", "Second Reminder"),
    ("TR", "Third Reminder"),
]

CREDITSTATUS = [
    ("PE", "Pending"),
    ("PY", "Paid"),
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
    TODO: Create a Partner for every User with Teacher tag on signal for
    linking it with the quotations
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
    """
    Dividend + Expenses + Assets = Liabilites + Owner Equity + Revenue
    |---------------------------|  |---------------------------------|
    Debits: Increase when debited  Credits: Increse when Credited
    and Decrease when credited     and Decresease when Debited

    Balance -> Credit or Debits Acording to squeme
    Book -> If an Book order is Asociated
    Partner -> For invoices not asociated with a book
    referral_code -> Security Code according to def invoice_pre_save_referenz()
    status -> needs to be balanced by the state_controller
    to_pay -> liability
    paid -> sum of payments
    pay_till -> due date
    pay_date -> date of last pay
    reminder_dates -> reminder dates Array
    methode -> Payment methode to track
    """
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

        if (self.paid is not None and self.pay_date is None) or (self.pay_date is not None and self.paid is None):
            raise ValidationError(_("Can't save. Paid invoices need a date and payment"))

        if self.status in ("PY", "ST"):
            if not self.methode or (self.methode == "UN"):
                raise ValidationError(_("Can't save. Paid invoices need a payment methode."))
            if self.paid is None or self.pay_date is None:
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


class Creditnote(models.Model):
    """
    @param
        invoice FK to invoice
        to_credit amount that has been credited from the price of booking
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    to_credit = models.DecimalField(max_digits=12, decimal_places=2)
    credited = models.DecimalField(max_digits=12, decimal_places=2)
    credit_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=10, choices=CREDITSTATUS, default="PE")
    created_on = models.DateTimeField(auto_now_add=True)


class Creditnotedate(models.Model):
    """
    Track of Canceled dates ?
    """
    creditnote = models.ForeignKey(Creditnote, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)


"""
# Only for Cycles

Before the beginning date of a cycle, due to limited spots and general organization of the class, we request\
    that you cancel the whole cycle at least 72 hours before the beginning of the cycle. This gives us \
    the opportunity to fill the free spot. You may cancel by email or online here. If you have to cancel your cycle\
    and you have not paid the invoice then there is no refund and no obligation of either part. If you paid the invoice\
    we offer you a credit to your account if you cancel before the 72 hours, but do not offer refunds.\
    These credit will be automatically used in the next booking of any class or event.\
    If you do not cancel the cycle prior to the 72 hours, class cancellation policies apply.

During the period of your cycle, if the corresponding invoice is paid, you may cancel up to one class.\
    Due to limited spots and general organization of the class, we request that you cancel at least 12 hours\
    before a scheduled class. This gives us the opportunity to fill or adapt the class. You may cancel by email\
    or online here. If you have to cancel your class, we offer you a credit to your account if you cancel\
    before the 12 hours, but do not offer refunds. These credit will be automatically used in the next booking\
    of any class or event. However, if you do not cancel prior to the 12 hours, you will lose the payment for the class.

Credit Conditions:

For all:
· You can only credit fully or partially a paid abo.
· Cancel the whole events is only posible till 72hrs before the first class.
· Cancel 1 class is only possible till 12hrs before the class.
· 1 date each 4 dates in the attendance, so doble cycles would have 2 classes.
· the credit must be used in the next booking
· will never be cashed out

0.- Check if abo is paid. Conditional offer credit or cancel.
1.- If first attd. > 72 hrs can be fully credited.
1.1.- Validate -> Check that conditions are still met.
1.2.- Creditnote.
2.- If first attd. < 72 hrs show avilable dates to credit. Only one can be selected in a radio form.
2.1.- Validate -> Check that conditions are still met.
2.2- Creditnote + Creditdate

3.- Open credit can be seen in profile
4.- When creating invoice check for open credits

5.- If CR < PO Invoice price = PO - Credit
6.- If CR > PO - 

"""
