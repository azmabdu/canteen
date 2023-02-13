from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    full_name = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password1', 'password2')

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
