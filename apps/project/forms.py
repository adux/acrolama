from dal import autocomplete
from tinymce.widgets import TinyMCE

from django import forms

from project.models import Event


class EventUpdateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            "price_options": autocomplete.ModelSelect2Multiple(
                url="po-autocomplete",
                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
            ),
            "time_locations": autocomplete.ModelSelect2Multiple(
                url="tl-autocomplete",
                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
            ),
            "irregularities": autocomplete.ModelSelect2Multiple(
                url="irregularities-autocomplete",
                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
            ),
            "teachers": autocomplete.ModelSelect2Multiple(
                url="teachers-autocomplete",
                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
            ),
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
