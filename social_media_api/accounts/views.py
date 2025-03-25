from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import CustomUserSerializer, UserLoginSerializer, TokenSerializer

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


