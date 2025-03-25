from django.urls import path
from .views import RegisterUserView, UserLoginView, UserListView

urlpatterns = [

    path('users/', UserListView.as_view(), name='list_users'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
]