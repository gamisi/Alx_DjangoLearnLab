from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

# BookSerializer to serialize Book model instances
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']  

    # Custom validation for the publication_year field to ensure it is not in the future.
    def validate_publication_year(self, value):
        current_year = datetime.now().year  # Get the current year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future. Current year is {current_year}.")
        return value


# AuthorSerializer to serialize Author model instances, including related Books
class AuthorSerializer(serializers.ModelSerializer):
    
    books = BookSerializer(many=True, read_only=True)  

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Including name of the author and a list of books

    
