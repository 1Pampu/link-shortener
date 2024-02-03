from django import forms
from .models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['original', 'short']

    def save(self, commit = True, user = None):
        instance = super().save(commit = False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance