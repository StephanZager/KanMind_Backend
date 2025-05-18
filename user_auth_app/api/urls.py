from django.urls import path
from .view import RegistrationView,LoginView,UsersView,EmailCheckView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UsersView.as_view(), name='users'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
