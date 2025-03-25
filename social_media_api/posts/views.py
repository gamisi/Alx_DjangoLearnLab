from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics
from .models import Post, Comment

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer