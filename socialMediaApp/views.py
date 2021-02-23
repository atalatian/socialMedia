from django.shortcuts import render , HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserForm


# Create your views here.
def index(request):
    return HttpResponse('ok')


class UserCreate(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('index')
    template_name = 'socialMediaApp/auth.html'

