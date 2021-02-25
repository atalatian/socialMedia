from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User
from .models import Post


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


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'description': forms.Textarea(),
        }
        error_messages = {
            'title': {
                'max_length': _("This Password is too long."),
            },
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'id': 'txtSearch'}))

