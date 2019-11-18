from django.db import models

INVOICESTATUS = [
    ("PE", "Pending"),
    ("PY", "Paid"),
    ("CA", "Canceled"),
    ("ST", "Storno"),
]
BALANCE = [("AS", "Assets"), ("EQ", "Equity"), ("LI", "Liabilities")]


METHODE = [
    ("BT", "Bank"),
    ("TW", "Twint"),
    ("PP", "PayPal"),
    ("CS", "Cash"),
    ("CR", "Credit Card"),
    ("UN", "Unclasified"),
]


class Account(models.Model):
    name = models.CharField(max_length=30)
    balance = models.CharField(max_length=11, choices=BALANCE)
    description = models.TextField(max_length=1000, null=True, blank=True)


class Partner(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    prefered_pay = models.CharField(
        max_length=15, choices=METHODE, null=True, blank=True
    )
    description_pay = models.TextField(max_length=15, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    book = models.ForeignKey(
        "booking.Book", null=True, blank=True, on_delete=models.CASCADE
    )
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=INVOICESTATUS, default="PE")
    amount = models.CharField(max_length=10)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )

    def __str__(self):
        if self.book:
            return "%s - %s" % (self.id, self.book)
        else:
            return "%s - %s" % (self.id, self.partner)


class Payment(models.Model):
    amount = models.CharField(max_length=9)
    pay_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    methode = models.CharField(
        max_length=15, choices=METHODE, default="UN", null=True, blank=True
    )
    degistered_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, null=True, blank=True, on_delete=models.CASCADE
    )
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    translation_amount = models.CharField(max_length=10)
    transaction_date = models.DateTimeField(auto_now_add=True)
