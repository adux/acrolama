# Django
from django import forms
from django.utils.translation import ugettext_lazy as _

# Models
from accounting.models import Invoice
from users.models import User
from booking.models import (
    Book,
    BookUserInfo,
    BookDuoInfo,
    BookDateInfo,
    Attendance,
    Quotation
)

# Services
from booking.services import book_is_paid

# Widgets
from herdi.widgets import (
    DynamicArrayWidget,
    M2MSelect,
    BootstrapedSelect2,
    BootstrapedSelect2Multiple,
)


def clean_booking(clean_data):
    event = clean_data.get('event')
    price = clean_data.get('price')
    times = clean_data.get('times')

    if len(times) > 1:
        raise forms.ValidationError("Error: Select only one time. Deprecated")

    event_to = [tl.time_option for tl in event.time_locations.all()]

    if times.first() not in event_to:
        raise forms.ValidationError("Error: Selected Time Option not in Event. Options are: {}".format(event_to))

    event_po = [po for po in event.price_options.all()]

    if price not in event_po:
        raise forms.ValidationError("Error: Selected Price not in Event. Options are: {}".format(event_po))

    return clean_data


class AttendanceUpdateForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ["attendance_date", "attendance_check"]
        widgets = {
            "attendance_check": DynamicArrayWidget(),
            "attendance_date": DynamicArrayWidget(),
        }


class BookUpdateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["user", "event", "status", "times", "comment", "comment_response", "note"]
        widgets = {
            "times": M2MSelect(),
            "event": BootstrapedSelect2(url="event-autocomplete"),
        }

    def clean(self):
        cleaned_data = super(BookUpdateForm, self).clean()
        new_status = cleaned_data.get('status')

        if (self.instance.status in ("IN", "PE", "WL", "CA", "SW")) and (new_status == "PA"):
            if not book_is_paid(self.instance.id):
                raise forms.ValidationError("Error: Cannot update to Participant. Invoice not paid.")

        return cleaned_data


class BookUserInfoUpdateForm(forms.ModelForm):

    class Meta:
        model = BookUserInfo
        fields = ["first_name", "last_name", "phone", "email"]

    def clean(self):
        cleaned_data = super(BookUserInfoUpdateForm, self).clean()

        for key, item in cleaned_data.items():
            if not item:
                raise forms.ValidationError("Error: {} can not be empty.".format(key))

        return cleaned_data


class BookDuoUpdateForm(forms.ModelForm):

    class Meta:
        model = BookDuoInfo
        fields = ["first_name", "last_name", "phone", "email"]


class BookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["user", "event", "times", "price"]
        widgets = {
            "times": M2MSelect(),
            "event": BootstrapedSelect2(url="event-autocomplete"),
            "user": BootstrapedSelect2(url="user-autocomplete",),
        }

    def clean(self):
        cleaned_data = super(BookCreateForm, self).clean()
        cleaned_data = clean_booking(cleaned_data)
        return cleaned_data


class TeacherBookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ["user", "event", "times", "price"]
        widgets = {
            "times": M2MSelect(),
            "event": BootstrapedSelect2(url="event-autocomplete"),
            "user": BootstrapedSelect2(url="user-autocomplete",),
        }


class QuotationCreateForm(forms.ModelForm):
    # TODO: On Model changes this line gives and error ... why?
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
            "admin_profit",
            "partner_profit",
        )
        widgets = {
            "teachers": BootstrapedSelect2Multiple(url="teachers-autocomplete"),
            "event": BootstrapedSelect2(url="event-autocomplete"),
            "time_location": BootstrapedSelect2(url="tl-autocomplete"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # NOT required
        self.fields["direct_costs"].required = False

        # disabledo
        self.fields["direct_revenue"].widget.attrs["readonly"] = True


class QuotationLockForm(forms.ModelForm):

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
            "admin_profit",
            "partner_profit",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["teachers"].queryset = User.objects.filter(is_teacher=True)
        self.fields["direct_costs"].queryset = Invoice.objects.filter(balance="DB")
        self.fields["direct_costs"].required = False

        if self.instance and self.instance.locked:
            self.fields['event'].disabled = True
            self.fields['time_location'].disabled = True
            self.fields['teachers'].disabled = True
            self.fields['related_rent'].disabled = True
            self.fields['direct_costs'].disabled = True
            self.fields['direct_revenue'].disabled = True
            self.fields['fix_profit'].disabled = True
            self.fields['admin_profit'].disabled = True
            self.fields['partner_profit'].disabled = True


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["times"].label_from_instance = lambda obj: "%s %s" % (
            obj.get_regular_day_display() if obj.regular_day else obj.name,
            obj.get_class_start_times() if obj.get_class_start_times() is not None else obj.get_open_start_times(),
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
        labels = {
            'first_name': "Partner First Name",
            'last_name': "Partner First Name",
            'phone': "Partner Phone ",
            'email': "Partner Email",
        }

    def clean_firstname(self):
        first_name = self.cleaned_data["first_name"]
        if first_name != "":
            return first_name[0].upper() + first_name[1:].lower()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if last_name != "":
            return last_name[0].upper() + last_name[1:].lower()
        return last_name

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email.lower()


class BookDateInfoForm(forms.ModelForm):

    class Meta:
        model = BookDateInfo
        exclude = ["book"]
