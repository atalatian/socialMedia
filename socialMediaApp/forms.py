from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User, Comment
from .models import Post
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
            'gender': forms.Select(choices=[(None, ''),
                                            ('male', 'Male'),
                                            ('female', 'Female')])
        }


class UserUpdateForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['email']
        widgets = {
            'gender': forms.Select(choices=[(None, ''),
                                            ('male', 'Male'),
                                            ('female', 'Female')])
        }


class UserEnterForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254)
    password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput)


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


class PostCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', ]
