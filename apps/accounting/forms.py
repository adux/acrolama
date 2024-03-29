import datetime
from django import forms
from accounting.models import Invoice
from booking.services import attendance_list_creditoptions


class InvoiceUpdateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ("paid", "pay_date", "methode", "status", "notes",)

    def clean(self):
        cleaned_data = super(InvoiceUpdateForm, self).clean()
        status = cleaned_data.get('status')

        if status in ("FR", "SR", "TR"):
            if self.instance.reminder_dates:
                if (status == "FR") and (len(self.instance.reminder_dates) == 1):
                    return cleaned_data
                if (status == "SR") and (len(self.instance.reminder_dates) == 2):
                    return cleaned_data
                if (status == "TR") and (len(self.instance.reminder_dates) == 3):
                    return cleaned_data
                if self.instance.reminder_dates[-1] + datetime.timedelta(2) > datetime.datetime.now().date():
                    raise forms.ValidationError("Wait 2 days to send next Reminder. Set correct status.")


class CreditnotedateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.book = args[1]
        super(CreditnotedateForm, self).__init__(*args, **kwargs)
        raw_choices = attendance_list_creditoptions(self.book.attendance.id)
        choices = []

        for i, v in enumerate(raw_choices):
            option = (f'{self.book.id}_{i}', v)
            choices.append(option)

        self.fields["radio"] = forms.ChoiceField(
            choices=choices,
        )
