from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser
from posts.models import Post
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomUserSerializer, UserLoginSerializer, TokenSerializer
from posts.serializers import PostSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RegisterUserView(generics.CreateAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [AllowAny]

    """def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({

                'message': 'User registered successfully!',
                'user': CustomUserSerializer(user).data

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

class UserLoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""#follow user function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user == user_to_follow:
        return Response({'detail': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Add the user to the following list
    user.following.add(user_to_follow)
    user_to_follow.followers.add(user)

    return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)

#unfollow user function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user == user_to_unfollow:
        return Response({'detail': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user from the following list
    user.following.remove(user_to_unfollow)
    user_to_unfollow.followers.remove(user)

    return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    # user = CustomUser
    user = request.user    
    # Get posts from the users the current user is following
    followed_users = user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)"""

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        if user == user_to_follow:
            return Response({'detail': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the following list and the target user to the followers list
        user.following.add(user_to_follow)
        user_to_follow.followers.add(user)

        return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        if user == user_to_unfollow:
            return Response({'detail': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the following list and the target user from the followers list
        user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(user)

        return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)


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