from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):

    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following']
        extra_kwargs = {'password': {'write_only': True}}
    
    """def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Create token when a new user is created
        return user"""

    def create(self, validated_data):
            # Extract followers data from validated_data
            followers_data = validated_data.pop('followers', [])
            following_data = validated_data.pop('following', [])
            # password = validated_data.pop('password', None)
            password = "12345678"
            # Create the user
            user = get_user_model().objects.create_user(**validated_data)
            if followers_data:
                user.followers.set(followers_data)
            if following_data:
                user.following.set(following_data)
            if password:
                user.set_password(password)  # Hash the password before saving
                user.save()
            Token.objects.create(user=user)
            return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

