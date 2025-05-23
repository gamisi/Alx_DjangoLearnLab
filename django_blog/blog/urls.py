from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, profile, home
from .import views
from .views import TaggedPostListView, PostByTagListView

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

    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'), # comment route
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),

    path('search/', views.search_posts, name='search_posts'),  # Search URL
    path('tags/<str:tag_name>/', views.PostListView.as_view(), name='posts_by_tag'),
    #path('posts/tag/<slug:tag>/', TaggedPostListView.as_view(), name='tagged_posts'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tagged_posts'),
        
]
