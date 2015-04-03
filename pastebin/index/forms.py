from django import forms

from pastebin.models import Paste


class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['title', 'content', 'visibility', 'users', 'syntax', 'expires_in']