from tinymce.widgets import TinyMCE

from django import forms

from project.models import Event

# Widgets
from booking.widgets import BootstrapedSelect2Multiple


class EventUpdateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            "price_options": BootstrapedSelect2Multiple(url="po-autocomplete",),
            "time_locations": BootstrapedSelect2Multiple(url="tl-autocomplete",),
            "irregularities": BootstrapedSelect2Multiple(url="irregularities-autocomplete",),
            "teachers": BootstrapedSelect2Multiple(url="teachers-autocomplete",),
            "description": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "prerequisites": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "highlights": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "included": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "food": TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }

    # def clean(self):
    #     cleaned_data = super(EventUpdateForm, self).clean()
    #     new_status = cleaned_data.get('status')

    #     if (self.instance.status in ("IN", "PE", "WL", "CA", "SW")) and (new_status == "PA"):
    #         # If invoice is not payed raise Error
    #         if not check_is_book_payed(self.instance.id):
    #             raise forms.ValidationError("Error: Cannot update to Participant. Invoice not payed.")
    #     return cleaned_data
