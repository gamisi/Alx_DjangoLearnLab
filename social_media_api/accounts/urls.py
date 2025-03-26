from django.urls import path
from .views import RegisterUserView, UserLoginView, UserListView
from .import views

urlpatterns = [

    path('users/', UserListView.as_view(), name='list_users'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),

    # followers and following urls
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('feed/', views.user_feed, name='user_feed'),
]