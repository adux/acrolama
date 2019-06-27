from django import forms
from django.utils.translation import ugettext_lazy as _
from booking.models import Book
from project.models import Event, PriceOption, TimeOption
from django.db import connection


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            slug = args[0]
            slug = slug.get("slug", "")
            if self.instance:
                self.fields["price"].queryset = PriceOption.objects.filter(
                    event__slug=slug
                )
                self.fields["time"].queryset = TimeOption.objects.filter(
                    timelocation__event__slug=slug
                )

    class Meta:
        model = Book
        fields = ("name", "email", "phone", "price", "time", "comment")
        labels = {
            "name": _(""),
            "email": _(""),
            "phone": _(""),
            "price": _(""),
            "time": _(""),
            "comment": _(""),
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full Name: Acro el lama"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email: acro@lama.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone: +41761234567"}),
            "price": forms.Select(attrs={"checked": "checked"}),
            "time": forms.Select(attrs={"checked": "checked"}),
            "comment": forms.Textarea(attrs={"placeholder": "Comment"}),
        }
        error_messages = {
            "name": {"required": _("")},
            "email": {"required": _("")},
            "phone": {"required": _("")},
            "time": {"required": _("Time preference:")},
            "price": {"required": _("Pricing preference:")},
        }
