from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
        error_messages = {
            'password': {
                'max_length': _("This Password is too long."),
            },
            'email': {
                'max_length': _("This Email is too long."),
            },
        }