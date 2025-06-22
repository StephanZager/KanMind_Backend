from django.urls import path
from .view import RegistrationView,LoginView,EmailCheckView,UserListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('users/', UserListView.as_view(), name='user-list')
    
]