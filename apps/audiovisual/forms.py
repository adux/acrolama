from django import forms

from audiovisual.models import Image


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['title', 'description', 'image']
