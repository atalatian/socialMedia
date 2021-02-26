from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signUp/', views.UserCreate.as_view(), name='signUp'),
    path('profile/<int:pk>', views.UserDetail.as_view(), name='profile'),
    path('profile/<int:pk>/createPost/', views.PostCreate.as_view(), name='createPost'),
    path('profile/<int:pk>/postDetail/<int:post_pk>', views.PostDetail.as_view(), name='postDetail'),
    path('view/<int:foreignUser_pk>/profile/<int:pk>', views.ViewUserDetail.as_view(), name='viewProfile'),
    path('view/<int:foreignUser_pk>/profile/<int:pk>/postDetail/<int:post_pk>',
         views.ViewPostDetail.as_view(), name='viewPostDetail'),
    path('logIn/', views.UserEnter.as_view(), name='logIn'),
    path('ajax_calls/search/', views.AutoCompleteView.as_view(), name='autocomplete'),
]


