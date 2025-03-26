from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, viewsets
from .models import Post, Comment
from rest_framework.response import Response
from rest_framework import status, permissions

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserFeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get posts from the users the current user is following
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    def get(self, request):
        # Use the `get_queryset` method to get the filtered posts
        posts = self.get_queryset()

        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)