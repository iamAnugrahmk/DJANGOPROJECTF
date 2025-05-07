from django import forms
from .models import Click, Profile

class ClickForm(forms.ModelForm):
    class Meta:
        model = Click
        fields = ['body']  # Include only the 'body' field for the form
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message here...'}),
        }

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