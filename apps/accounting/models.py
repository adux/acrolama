from django.db import models

INVOICESTATUS = [
    ("PE", "Pending"),
    ("PY", "Paid"),
    ("CA", "Canceled"),
    ("ST", "Storno"),
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
]

class Partner(models.Model):
    name = models.CharField(max_length=50)
    address = models.ForeignKey(
        "address.Address", null=True, blank=True, on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    iban = models.CharField(max_length=50, null=True, blank=True)
    swift = models.CharField(max_length=50, null=True, blank=True)
    prefered_pay = models.CharField(
        max_length=15, choices=METHODE, null=True, blank=True
    )
    notes = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    balance = models.CharField(max_length=11, choices=BALANCE)
    book = models.OneToOneField(
        "booking.Book", null=True, blank=True, on_delete=models.CASCADE
    )
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, null=True, blank=True
    )
    referral_code = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=INVOICESTATUS, default="PE"
    )
    to_pay = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )

    pay_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )

    methode = models.CharField(
        max_length=15, choices=METHODE, default="UN", null=True, blank=True
    )
    notes = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.book:
            return "%s - %s" % (self.id, self.book)
        else:
            return "%s - %s" % (self.id, self.partner)
