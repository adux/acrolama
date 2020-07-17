from django import forms


from accounting.models import Invoice


class UpdateInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("paid", "pay_date", "methode", "status", "notes")
