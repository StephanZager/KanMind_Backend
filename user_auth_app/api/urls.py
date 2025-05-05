from django.urls import path
from .view import RegistrationView,UserProfileList,UserProfileDetail

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'),
    path('users/', UserProfileList.as_view(), name= 'users'),
    path('users/<int:pk>', UserProfileDetail.as_view(), name= 'users-details')
]