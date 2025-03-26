from django.urls import path, include
from .views import PostListCreateView, CommentListCreateView, PostViewset, CommentViewset, UserFeedView
from rest_framework.routers import DefaultRouter
from .import views

# Create a router and register your viewset
router = DefaultRouter() #define router
router.register(r'posts_all', PostViewset, basename='posts_all')
router.register(r'comments_all', CommentViewset, basename='comments_all')

urlpatterns = [

    path('api/', include(router.urls)),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('feed/', UserFeedView.as_view(), name='user_feed'),
    path('like/<int:post_id>/', views.LikePostView.as_view(), name='like_post'),
    path('unlike/<int:post_id>/', views.UnlikePostView.as_view(), name='unlike_post'),

]