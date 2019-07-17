from django import forms
from django.contrib.auth.forms import UserCreationForm
from registration.forms import RegistrationForm

from .models import Player


class PlayerRegistrationForm(RegistrationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', strip=False, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = Player
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': '',
        }
