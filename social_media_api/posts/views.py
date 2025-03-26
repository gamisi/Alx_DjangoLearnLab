from django.shortcuts import render
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, viewsets
from .models import Post, Comment, Like
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from notifications.views import create_notification
from rest_framework.views import APIView
from notifications.models import Notification

# Create your views here.

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve all comments for the specified post_id
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(id=post_id)

    def post(self, request, post_id):
        user = request.user
        post = Post.objects.get(id=post_id)
        comment_text = request.data.get('comment')

        # Create Comment
        comment = Comment.objects.create(user=user, post=post, text=comment_text)

        # Create a notification for the post author
        create_notification(user, post.author, 'commented on your post', post)

        return Response({'detail': 'Comment added successfully'}, status=200)

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

# Like Post View
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = generics.get_object_or_404(Post, pk=pk)

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a Like record
        like = Like.objects.get_or_create(user=request.user, post=post)

        # Generate a notification for the post author
        # create_notification(user, post.author, 'liked', post)

        Notification.objects.create(user, post.author, 'liked', post)

        return Response({'detail': 'Post liked successfully'}, status=status.HTTP_201_CREATED)

# Unlike Post View
class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, id=pk)

        # Check if the user has liked the post
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the Like
        like.delete()

        # Optional: If you want to generate a notification for unlike action, you can modify the logic here.
        # In most cases, you might not need a notification for unliking, but you can still create one if needed.
        return Response({'detail': 'Post unliked successfully'}, status=status.HTTP_200_OK)