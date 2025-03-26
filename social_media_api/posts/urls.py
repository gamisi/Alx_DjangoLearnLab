from django.urls import path, include
from .views import PostListCreateView, CommentListCreateView, PostViewset, CommentViewset
from rest_framework.routers import DefaultRouter

# Create a router and register your viewset
router = DefaultRouter() #define router
router.register(r'posts_all', PostViewset, basename='posts_all')
router.register(r'comments_all', CommentViewset, basename='comments_all')

urlpatterns = [

    path('api/', include(router.urls)),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),

]