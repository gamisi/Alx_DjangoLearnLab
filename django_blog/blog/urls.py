from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, profile, home
from .import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Registration and profile
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path ('home/', home, name='home'),
    #path('posts/', posts, name='posts'),

    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
        
]
