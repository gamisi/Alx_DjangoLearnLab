from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, profile, home, posts

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

     path('logout/', LogoutView.as_view(), name='logout'),

    # Registration and profile
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path ('home/', home, name='home'),
    path('posts/', posts, name='posts')
        
]
