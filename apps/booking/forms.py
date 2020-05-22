from dal import autocomplete
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

# Models
from accounting.models import Invoice
from users.models import User
from project.models import Event, PriceOption, TimeOption
from booking.models import BOOKINGSTATUS, Book, BookDuoInfo, BookDateInfo, Attendance, Quotation

from booking.widgets import DynamicArrayWidget, M2MSelect


class UpdateAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["attendance_date", "attendance_check"]
        widgets = {
            "attendance_check": DynamicArrayWidget(),
            "attendance_date": DynamicArrayWidget(),
        }


class UpdateBookForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[(k, v) for k, v in BOOKINGSTATUS if k not in "PA"])

    class Meta:
        model = Book
        fields = ["user", "event", "status", "times"]
        widgets = {"times": forms.CheckboxSelectMultiple}


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["user", "event", "times", "price"]
        widgets = {"times": forms.CheckboxSelectMultiple}


class CreateQuotationForm(forms.ModelForm):
    direct_costs = forms.MultipleChoiceField(
        choices=[("%s %s" % (o.id, o.to_pay), o.__str__) for o in Invoice.objects.filter(balance="DB")]
    )

    class Meta:
        model = Quotation
        fields = (
            "event",
            "time_location",
            "teachers",
            "related_rent",
            "total_attendees",
            "direct_revenue",
            "fix_profit",
            "acrolama_profit",
            "teachers_profit",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filled
        self.fields["teachers"].queryset = User.objects.filter(is_teacher=True)

        # NOT required
        self.fields["direct_costs"].required = False

        # disabledo
        self.fields["direct_revenue"].widget.attrs["readonly"] = True


class LockQuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = (
            "event",
            "time_location",
            "teachers",
            "related_rent",
            "direct_costs",
            "direct_revenue",
            "fix_profit",
            "acrolama_profit",
            "teachers_profit",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teachers"].queryset = User.objects.filter(is_teacher=True)
        self.fields["direct_costs"].queryset = Invoice.objects.filter(balance="DB")


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["times"].label_from_instance = lambda obj: "%s %s" % (
            obj.regular_days if obj.regular_days else obj.name,
            obj.get_class_start_times() if obj.get_class_start_times is not None else obj.get_open_start_times(),
        )
        self.fields["price"].empty_label = "Select a Pricing Option"
        self.fields["times"].empty_label = None
        self.fields["accepted_policy"].required = True

    class Meta:
        model = Book
        fields = ["times", "price", "comment", "accepted_policy"]
        labels = {"price": _(""), "times": _(""), "comment": _("")}
        widgets = {
            "price": forms.Select(attrs={"checked": "checked"}),
            "times": M2MSelect(attrs={}),
            "comment": forms.Textarea(attrs={"placeholder": "Comment"}),
        }

    # TODO: Clean times to only be part of Event


class BookDuoInfoForm(forms.ModelForm):
    class Meta:
        model = BookDuoInfo
        fields = ["first_name", "last_name", "phone", "email"]

    def clean_firstname(self):
        first_name = self.cleaned_data["first_name"]
        if first_name is not "":
            return first_name[0].upper() + first_name[1:].lower()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if last_name is not "":
            return last_name[0].upper() + last_name[1:].lower()
        return last_name

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email.lower()


class BookDateInfoForm(forms.ModelForm):
    class Meta:
        model = BookDateInfo
        exclude = ["book"]
