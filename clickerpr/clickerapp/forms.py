from django import forms
from .models import Click, Profile

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

# Add a form for updating the Profile model
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        max_length=160,  # Enforce a maximum of 160 characters
        widget=forms.Textarea(attrs={
            'placeholder': 'Write something about yourself...',
            'class': 'form-control',
            'rows': 3,
            'maxlength': '160',  # Add maxlength attribute to the HTML
        }),
        label="Bio",
    )

    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']