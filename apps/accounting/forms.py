from django import forms
from django.utils.translation import ugettext_lazy as _


from accounting.models import Invoice


class UpdateInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("paid", "pay_date", "methode", "status")
