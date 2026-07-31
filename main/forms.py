from django import forms 
from django.contrib.auth.models import User 

class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder':"Complete Name"})
    )
    username_or_email = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder':"Username or email address"})
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder':"Password"})
    )
    
    def clean_username_or_email(self):
        val = self.cleaned_data.get('username_or_email').strip()
        # Check if username or email is already taken
        if User.objects.filter(username__iexact=val).exists() or User.objects.filter(email__iexact=val).exists():
            raise forms.ValidationError("This username or email is already registered.")
        return val
    

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':"Username or email address"})
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':"Password"})
    )
    remember_me = forms.BooleanField(required=False)