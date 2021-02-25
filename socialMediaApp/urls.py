from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp/', views.UserCreate.as_view(), name='signUp'),
    path('profile/<int:pk>', views.UserDetail.as_view(), name='profile'),
    path('profile/<int:pk>/createPost/', views.PostCreate.as_view(), name='createPost'),
    path('profile/<int:pk>/postDetail/<int:post_pk>', views.PostDetail.as_view(), name='postDetail'),
    path('logIn/', views.UserEnter.as_view(), name='logIn'),
    path('ajax_calls/search/', views.AutoCompleteView.as_view(), name='autocomplete'),
    path('search/', views.SearchView.as_view(), name='search'),
]


