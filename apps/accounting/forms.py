from django import forms


from accounting.models import Invoice


class InvoiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("paid", "pay_date", "methode", "status", "notes")
