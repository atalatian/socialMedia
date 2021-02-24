from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp/', views.UserCreate.as_view(), name='signUp'),
    path('profile/<int:pk>', views.UserDetail.as_view(), name='profile'),
    path('logIn/<str:state>', views.UserEnter.as_view(), name='logIn'),
]


