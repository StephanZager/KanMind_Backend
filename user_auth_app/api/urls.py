from django.urls import path
from .view import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
]