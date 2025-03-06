from rest_framework import serializers
from .models import Book
from .models import Author
from datetime import datetime


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields= ['name', 'bio']

class BookSerializer(serializers.ModelSerializer):

    author = AuthorSerializer() #nested serializer

    days_since_created = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'created_at', 'days_since_created']

    def get_days_since_created(self, obj):
        # Calculate the number of days since the book was created
        today = datetime.now().date()
        days_since = (today - obj.created_at.date()).days  # Calculate the difference in days
        return days_since

    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError("Name must be at least 5 characters long.")
        return data

    def create(self, validated_data):
        # Extract the author data from the validated data
        author_data = validated_data.pop('author')

        # Check if the author already exists by name or create a new one
        author, created = Author.objects.get_or_create(

            name=author_data['name'],  # Assuming 'name' is unique, adjust if necessary
            defaults={'bio': author_data.get('bio', '')}  # Only set bio if it's provided

        )

        # Create the book and associate the author
        book = Book.objects.create(author=author, **validated_data)        
        return book

    
