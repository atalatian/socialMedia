from django.contrib.auth import login
import random
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import User


def myLogin(request, user):
    myUser = User.objects.get(djangoUser=user)
    if myUser.verified:
        login(request, user)
        return True
    else:
        return False
