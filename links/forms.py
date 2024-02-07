from django import forms
from .models import Link
from django.core.exceptions import ValidationError

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['original', 'short']

    original = forms.CharField(label='Paste the URL here:',
                               widget=forms.TextInput(attrs={'placeholder': 'https://'}))
    short = forms.CharField(label='https://shortly.com/li/', label_suffix=" ",
                            widget=forms.TextInput(attrs={'placeholder': 'Custom link'}),
                            required=False)

    def clean_short(self):
        short = self.cleaned_data['short']

        if Link.objects.filter(short=short).exists():
           raise ValidationError("This Link already exists. Please choose another one.")

        if " " in short:
            raise ValidationError("The short link cannot contain spaces")

        if "/" in short:
            raise ValidationError("The short link cannot contain '/'")

        if "?" in short:
            raise ValidationError("The short link cannot contain '?'")

        if "%" in short:
            raise ValidationError("The short link cannot contain '%'")

        return short