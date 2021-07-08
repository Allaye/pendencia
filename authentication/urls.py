from django.urls import path
from rest_framework.generics import ListAPIView
from authentication import views

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('user/', views.AuthUserApiView.as_view(), name='user')
]