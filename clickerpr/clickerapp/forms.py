from django import forms
from .models import Click

class clickForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Click here to add a click message',
            'class': 'form-control',
            'rows': 3,
        }),
        label="",
    )

    class Meta:
        model = Click
        exclude = ('user',)
