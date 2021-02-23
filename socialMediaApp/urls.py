from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.UserCreate.as_view(), name='userCreate'),
]
