from django import forms
from .models import Click, Profile

class ClickForm(forms.ModelForm):
    class Meta:
        model = Click
        fields = ['body', 'image','video'] 
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message here...'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']  