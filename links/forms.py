from django import forms
from .models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['original', 'short']

    original = forms.CharField(label='Paste the URL here:',
                               widget=forms.TextInput(attrs={'placeholder': 'https://'}))
    short = forms.CharField(label='https://shortly.com/li/', label_suffix=" ",
                            widget=forms.TextInput(attrs={'placeholder': 'Custom link'}),
                            required=False)