from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from pastebin.models import Paste  # @UnresolvedImport


class PasteForm(forms.ModelForm):

    class Meta:
        model = Paste
        fields = ['title', 'content', 'visibility', 'users', 'syntax', 'expires_in']

    def __init__(self, user, *args, **kwargs):
        super(PasteForm, self).__init__(*args, **kwargs)
        
        self.user = user;
        self.fields['users'].queryset = User.objects.exclude(pk=self.user.pk)

    def clean(self):
        cleaned_data = super(PasteForm, self).clean()

        visibleForUsers = cleaned_data.get('visibility') == Paste.ONLY_SPECIFIED_USERS        
        areNoUsers = len(cleaned_data.get('users')) == 0
        
        if visibleForUsers and areNoUsers:
            raise ValidationError("At least one user is required")
