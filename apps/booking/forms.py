from django import forms
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


from accounting.models import Invoice
from users.models import User

from booking.models import Book, Attendance, Quotation
from booking.widgets import DynamicArrayWidget


from project.models import PriceOption, TimeOption


class UpdateAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("attendance_date", "attendance_check")
        widgets = {
            "attendance_check": DynamicArrayWidget(),
            "attendance_date": DynamicArrayWidget(),
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("user", "event", "status", "times")
        widgets = {"times": forms.CheckboxSelectMultiple}


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("user", "event", "times", "price")
        widgets = {"times": forms.CheckboxSelectMultiple}


class CreateQuotationForm(forms.ModelForm):
    direct_costs = forms.MultipleChoiceField(
        choices=[
            ["%s %s" % (o.id, o.to_pay), o.__str__]
            for o in Invoice.objects.filter(balance='DB')
        ]
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

        #NOT required
        self.fields["direct_costs"].required=False

        #disabled
        self.fields["direct_revenue"].disabled=True
        # self.fields["acrolama_profit"].disabled=True
        # self.fields["teachers_profit"].disabled=True



class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            # Args from view, since its a tuple need to get the position and
            # then get slug from the dictionary
            # not sure how to improve this. Don't understand the whole Form
            # Schizzle yet
            slug = args[0].get("slug")
            if self.instance:
                self.fields["price"].queryset = PriceOption.objects.filter(
                    event__slug=slug
                )
                self.fields["times"].queryset = TimeOption.objects.filter(
                    timelocation__event__slug=slug
                )
                self.fields["times"].label_from_instance = (
                    lambda obj: "%s %s"
                    % (
                        obj.regular_days if obj.regular_days else obj.name,
                        obj.get_class_start_times()
                        if obj.get_class_start_times
                        else obj.get_open_start_times(),
                    )
                )
                self.fields["price"].empty_label = "Select a Pricing Option"
                self.fields["times"].empty_label = None

    class Meta:
        model = Book
        fields = ("times", "price", "comment")
        labels = {"price": _(""), "times": _(""), "comment": _("")}
        widgets = {
            "price": forms.Select(attrs={"checked": "checked"}),
            "times": forms.CheckboxSelectMultiple(attrs={}),
            "comment": forms.Textarea(
                attrs={"cols": 35, "rows": 5, "placeholder": "Comment"}
            ),
        }
        error_messages = {
            "times": {"required": _("Time preference:")},
            "price": {"required": _("Pricing preference:")},
        }

    def clean(self):
        # run the standard clean method first
        cleaned_data = super(BookForm, self).clean()
        times_verify = cleaned_data.get("times")
        # always return the cleaned data
        return cleaned_data

