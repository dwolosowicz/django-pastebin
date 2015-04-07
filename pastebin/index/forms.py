from django.core.exceptions import ValidationError
from django import forms

from pastebin.models import Paste


class PasteForm(forms.ModelForm):

    class Meta:
        model = Paste
        fields = ['title', 'content', 'visibility', 'users', 'syntax', 'expires_in']

    def clean(self):
        cleaned_data = super(PasteForm, self).clean()

        if cleaned_data.get('visibility') == Paste.ONLY_SPECIFIED_USERS and len(cleaned_data.get('users')) == 0:
             raise ValidationError("At least one user is required")
