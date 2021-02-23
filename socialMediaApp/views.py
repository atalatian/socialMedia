from django.shortcuts import render, reverse, HttpResponse
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserForm


# Create your views here.
def index(request):
    return HttpResponse('ok')


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    template_name = 'socialMediaApp/auth.html'
    success_url = reverse('index')
