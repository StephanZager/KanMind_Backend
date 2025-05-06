from django.urls import path
from .view import RegistrationView, UserProfileList, UserProfileDetail
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login')
]
