from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User, Comment
from .models import Post
from django.contrib.auth.models import User as DjangoUser

from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control'}))
    phoneNumber = forms.CharField(max_length=255, required=True, label="Phone Number"
                                  , widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               , max_length=255, required=True)
    firstName = forms.CharField(max_length=255, required=False, label="First Name"
                                , widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(max_length=255, required=False, label="Last Name",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=[(None, ''),
                                                          ('male', 'Male'),
                                                          ('female', 'Female')]), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    website = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    loginWithPhoneNumber = forms.BooleanField(required=False,
                                              label="Login With Phone Number?",
                                              widget=forms.CheckboxInput(
                                                  attrs={"disabled": "true", 'class': 'form-check-input'}))


class UserUpdateForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               max_length=255, required=False)
    firstName = forms.CharField(max_length=255, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(max_length=255, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=[(None, ''),
                                                          ('male', 'Male'),
                                                          ('female', 'Female')]), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    website = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)



class UserEnterForm(forms.Form):
    username = forms.CharField(required=True, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(required=True, max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {
                'max_length': _("This Password is too long."),
            },
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255, label='',
                             widget=forms.TextInput(attrs={'id': 'txtSearch',
                                                           'placeholder': 'Search',
                                                           'class': 'mb-0 form-control'}))


class tokenForm(forms.Form):
    token = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))


class PostCommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
        fields = ['body', ]
